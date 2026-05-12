from __future__ import annotations

from domain.chapter.models import ChapterDraft, ChapterEvent


CHAPTER_TWO_TEXT = """# 第二章 盐镜里的证词

夏葵讨厌不会停的东西。

潮声不会停，债主的账本不会停，母亲夜里重复同一句话的声音也不会停。可她必须把那面盐镜送过三道水闸，交给一个连名字都不肯写在纸上的买家。

蓝蜡商会给她的工具是一只铜盒。盒子里没有发条，没有煤油，也没有能装电池的暗格，只有一枚细得像鱼刺的摆轮。管事把它推到她面前时，只说这东西能让旧水闸自己咬住齿轨，足够她从巡灯船眼皮底下过去。

“它烧什么？”夏葵问。

管事笑了笑：“聪明人才会问这个。更聪明的人不会问第二遍。”

现在，夏葵站在第三水闸的阴影里，终于明白为什么。

摆轮一放进潮汐铜凹槽，整座旧闸机就动了起来。铁齿互相咬合，闸链慢慢绷直，沉重的水门无声抬起。没有蒸汽，没有人力，没有火焰，连摩擦声都像被某种东西提前拿走。

如果只看表面，它就是传闻里的永动机。

可夏葵的视线忽然断了一下。

上一刻，巡灯船还在桥洞外。下一刻，船灯已经擦着她的肩头过去，水面多了七圈扩散开的涟漪。她知道自己没有昏迷，也没有眨眼。只是有七分钟从她身上被抽走了，像有人从布匹中间剪下一段，再把两头粗暴缝合。

盐镜在怀里发烫。

镜面浮出一行模糊字迹：第十一次报点之后，证人夏葵离开西码头。

她盯着自己的名字，第一次感到这趟委托不是送货，而是把自己送进某份早已写好的证词里。

远处传来封锁哨。潮钟署的人比约定更快。

夏葵把铜盒合上，闸机立刻停住，像刚才那段无燃料运转从没发生过。她没有多看一眼。未来七分钟已经付出去了，再心疼也不能退货。母亲的治疗契约还压在蓝蜡商会手里，她没有资格把代价算得太细。

她沿着排水梯钻进下层暗渠，盐镜贴着胸口，一下又一下地发热。

镜中那行字却变了：

证人夏葵没有离开西码头。
"""


def build_chapter_two_draft() -> ChapterDraft:
    return ChapterDraft(
        id="chapter_002",
        title="盐镜里的证词",
        viewpoint_character_ids=["xia_kui"],
        text=CHAPTER_TWO_TEXT,
        events=[
            ChapterEvent(
                id="c002_e001",
                viewpoint_character_id="xia_kui",
                actor_id="xia_kui",
                event_type="delivery",
                description="Xia carries the salt mirror through the canal route for the Blue Wax Guild.",
                used_information=["salt_mirror_testimony"],
                uncertain_information=["salt_mirror_testimony"],
                supports_actor_goal=True,
                time_spent=1,
                minimum_time_required=1,
            ),
            ChapterEvent(
                id="c002_e002",
                viewpoint_character_id="xia_kui",
                actor_id="xia_kui",
                event_type="device_activation",
                description="Xia activates the perpetual pendulum to move the water lock without visible fuel.",
                used_information=["perpetual_pendulum_rumor"],
                uncertain_information=["perpetual_pendulum_rumor"],
                used_skills=["perpetual_pendulum"],
                consumed_resources={"future_minutes": 7},
                triggered_hard_rule_ids=["perpetual_motion_debt"],
                hard_rule_effects_applied=["perpetual_motion_debt"],
                dangerous_information_consequences=["perpetual_pendulum_rumor"],
                supports_actor_goal=True,
                time_spent=1,
                minimum_time_required=1,
            ),
            ChapterEvent(
                id="c002_e003",
                viewpoint_character_id="xia_kui",
                actor_id="xia_kui",
                event_type="revelation",
                description="The salt mirror changes its testimony and implicates Xia in mutually exclusive records.",
                used_information=["salt_mirror_testimony"],
                uncertain_information=["salt_mirror_testimony"],
                information_gained=["salt_mirror_testimony"],
                dangerous_information_consequences=["salt_mirror_testimony"],
                supports_actor_goal=True,
            ),
        ],
    )
