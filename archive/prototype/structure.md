┌─────────────────────────────────────────────┐
│   WMS（仓库管理系统）                       │
│   - 手握全天所有订单                        │
│   - 决定如何分组、什么时候推送              │  ← 上层决策（Tactical）
└─────────────────────────────────────────────┘
                    │
                    │ 推送 Wave 1, Wave 2, Wave 3...
                    ↓
┌─────────────────────────────────────────────┐
│   Fleet Scheduler                           │
│   - 收到 wave 后，决定哪个订单给哪台 AMR    │  ← 下层决策（Operational）
└─────────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────┐
│   AMR Fleet（20-50 台机器人）               │
│   - 执行订单                                │
│   - 跨层必须争用电梯                        │
└─────────────────────────────────────────────┘
                    │
                    ↓
        ┌────────────────────┐
        │  共享电梯（瓶颈）   │
        └────────────────────┘

Wave = {
    orders: [order_1, order_2, ..., order_k],   # 哪些订单一起释放
    release_time: τ                              # 在什么时刻释放
}

@dataclass
class Order:
    id: int
    source_floor: int   # 起点楼层
    dest_floor: int     # 终点楼层
    release_time: float

@dataclass
class Wave:
    orders: List[Order]     # 这个 wave 包含哪些 orders
    release_time: float     # 这个 wave 什么时候释放


你的三维特征 (C,I,T) 描述的就是"这个 wave 长什么样"：
C：这个 wave 里的 orders 涉及的楼层分布如何
I：这个 wave 里向上/向下的比例
T：这个 wave 里 orders 的释放时间是否集中（v0.1 里固定为 0，意味着 wave 内所有 orders 同时释放）