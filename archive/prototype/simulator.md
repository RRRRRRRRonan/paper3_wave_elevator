Simulator 的完整执行顺序
初始状态（t = 0）
5 个 AMR：全部在 1 楼，空闲，t = 0
1 个 Elevator：在 1 楼，空闲，available_at = 0
主循环：按 wave.orders 的顺序，一个一个处理订单
这是关键——simulator 不是并发模型，而是顺序遍历订单。
每个 order 的处理分4 个阶段：

Phase 1: 分配 AMR
python
    amr = min(amrs, key=lambda a: a.current_time)
    t = amr.current_time
规则：选出当前最早空闲的 AMR。如果多个 AMR 同时空闲（比如都在 t=0），选 id 最小的。
t = 这个 AMR 当前可用的时刻。

Phase 2: AMR 移动到 source floor（如果需要）
python
    if amr.current_floor != order.source_floor:
    t = elevator.request(amr.current_floor, order.source_floor, t)
    amr.current_floor = order.source_floor
条件：只有当 AMR 不在 source floor 时，才用电梯。
如果 AMR 已经在 source floor（比如第一个订单是 1→X，AMR 初始就在 1 楼）→ 跳过 Phase 2。

Phase 3: Pickup
python
    t += service_time  # 5 秒
无条件加 5 秒。AMR 完成 pickup，时刻变 t。

Phase 4: AMR 送货到 dest floor（如果需要）
python
    if order.source_floor != order.dest_floor:
    t = elevator.request(order.source_floor, order.dest_floor, t)
    amr.current_floor = order.dest_floor
条件：只有当 source ≠ dest 时用电梯。same-floor order 直接跳过。

Phase 5: Dropoff
python
    t += service_time  # 5 秒
    amr.current_time = t
AMR 完成 dropoff，时刻变 t。更新 AMR 的 current_time——这是下一次 AMR 被选中时的 t 起点。

Elevator 请求的内部逻辑（Phase 2 和 Phase 4 都调用）
这是最复杂的部分——电梯不是瞬时响应，它有自己的状态。
python
    def request(self, amr_current_floor, target_floor, request_time):
    wait_start = max(request_time, self.available_at)
    reposition_time = abs(self.current_floor - amr_current_floor) * 5
    loading_end = wait_start + reposition_time + 2
    travel_time = abs(amr_current_floor - target_floor) * 5
    arrive_at_target = loading_end + travel_time
    unloading_end = arrive_at_target + 2
    
    self.current_floor = target_floor
    self.available_at = unloading_end
    
    return unloading_end

电梯一次服务分 5 步：
步骤           说明                                        耗时
(a) Wait       AMR 和电梯中较晚到达的一方等另一方        max(request_time, elevator.available_at)- request_time 或 0
(b) Reposition 电梯从当前位置空驶到 AMR 所在层          |elevator.current_floor - amr_floor| × 5
(c) Loading    AMR 上电梯                              2 秒
(d) Travel     电梯载着 AMR 到 target                  |amr_floor - target_floor| × 5
(e) Unloading  AMR 下电梯                              2 秒

返回值：AMR 下电梯的时刻（= unloading_end）
副作用：电梯的 current_floor 更新为 target；available_at 更新为 unloading_end。

