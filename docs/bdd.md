{
  "spec_version": "1.0",
  "description": "BDD 验收场景。每个产出单元（事件、章节、图谱片段）必须通过所有相关场景。",
  
  "scenarios": [
    {
      "id": "A.1",
      "name": "反派决策一致性",
      "applies_to": ["graph_construction", "chapter_generation"],
      "given": "反派角色 X 与主角 Y 相遇",
      "and_given": ["X 不知道 Y 是'主角'"],
      "when": "X 评估 Y 的威胁等级并做出反应",
      "then": [
        "X 的反应基于其当时掌握的信息（X.PerspectiveView）",
        "不能因为 Y 是主角而高估或低估",
        "决策必须在 X.core_desire 体系下合理"
      ],
      "failure_criteria": "决策不能用 X 的信息和目标解释"
    },
    {
      "id": "A.2",
      "name": "反派信息对称性",
      "applies_to": ["chapter_generation"],
      "given": "反派 X 拥有资源/手段 R",
      "and_given": ["R 在当前情境下对 X 可用"],
      "when": "X 面对一个能用 R 解决的问题",
      "then": [
        "X 必须考虑使用 R",
        "不使用 R 必须有 X 内部的合理理由"
      ],
      "failure_criteria": "X 不用 R 的原因来自'作者不让用'而非角色逻辑"
    },
    {
      "id": "A.3",
      "name": "反派目标自洽",
      "applies_to": ["graph_construction", "chapter_generation"],
      "given": "反派 X 有明确长期目标 G",
      "when": "X 做出任何重要决策",
      "then": [
        "决策应服务于 G",
        "偏离 G 必须有 X 内部的动机解释"
      ]
    },
    
    {
      "id": "B.1",
      "name": "实力差距硬约束",
      "applies_to": ["chapter_generation"],
      "given": "主角 Y 实力为 L1，对手 X 实力为 L2，L2 >> L1",
      "when": "Y 与 X 直接冲突",
      "then": [
        "Y 不能通过'突然觉醒'或'莫名变强'赢",
        "Y 要么合理地输（受伤、逃跑、被俘）",
        "Y 要么用合乎世界规则的方式取胜：环境、信息差、第三方、付代价的孤注一掷",
        "取胜方式必须能写成因果链，每环站得住"
      ],
      "validator": "trace_causal_chain(victory_event)"
    },
    {
      "id": "B.2",
      "name": "主角死亡可能性",
      "applies_to": ["chapter_generation"],
      "given": "主角 Y 触发硬规则 R 中的死亡条件",
      "when": "条件在其他角色身上会导致死亡",
      "then": [
        "Y 也必须死，或付出等价代价",
        "不能因为是主角豁免"
      ]
    },
    {
      "id": "B.3",
      "name": "奇遇的稀缺性与代价",
      "applies_to": ["graph_construction", "chapter_generation"],
      "given": "主角 Y 获得机缘 M",
      "when": "M 被纳入 Y 的能力体系",
      "then": [
        "M 的来源必须是世界中真实存在的因果链",
        "M 的获得必须有代价（COSTS 边）",
        "M 的稀缺性必须能解释为什么是 Y 拿到",
        "若是巧合，'巧合'概率必须在世界规则允许范围内"
      ]
    },
    
    {
      "id": "C.1",
      "name": "每个视角角色都是主角",
      "applies_to": ["chapter_generation"],
      "given": "从角色 C 视角叙述",
      "when": "叙述发生在 C 视角的段落",
      "then": [
        "C 必须有自己的目标、思考、情感",
        "其他角色在该段中应相对扁平化",
        "读者应感受到 C 是这段的中心",
        "C 不应被用作'为主角传达信息的工具'"
      ]
    },
    {
      "id": "C.2",
      "name": "罗生门式真相",
      "applies_to": ["multi_perspective_chapter"],
      "given": "事件 E 发生时多个视角角色在场",
      "when": "从其中至少两个角色视角分别叙述 E",
      "then": [
        "不同版本之间必须存在矛盾或差异",
        "每个版本在该角色视图内必须自洽",
        "矛盾源于：信息差、立场差、心境差、感官差、记忆扭曲——非作者随意",
        "读者不应能仅凭任一版本判断完整真相"
      ],
      "validator": "diff_check(version_A, version_B) > threshold"
    },
    {
      "id": "C.3",
      "name": "阅读顺序无关性",
      "applies_to": ["full_novel"],
      "given": "新读者从角色 C 的故事线开始读",
      "when": "读者读完 C 的完整故事线",
      "then": [
        "应获得完整、自洽的故事体验",
        "不需要前置阅读其他角色线",
        "核心冲突、世界观、C 的弧光都清晰"
      ]
    },
    
    {
      "id": "D.1",
      "name": "资源守恒",
      "applies_to": ["graph_construction", "chapter_generation"],
      "given": "角色 C 从 L1 突破到 L2",
      "when": "突破完成",
      "then": [
        "必须追溯到具体资源消耗（CONSUMES 边）",
        "资源在世界中有限",
        "消耗使其他角色少拥有该资源（若共享池）",
        "消耗记录在角色档案可追溯"
      ],
      "validator": "verify_resource_balance(before, after)"
    },
    {
      "id": "D.2",
      "name": "时间真实性",
      "applies_to": ["chapter_generation"],
      "given": "突破/学新技能 S 通常需要时间 T",
      "when": "角色 C 完成 S",
      "then": [
        "C 投入的时间 >= T，或",
        "有可解释的压缩因素，且因素在世界规则下成立"
      ]
    },
    {
      "id": "D.3",
      "name": "强度上限",
      "applies_to": ["chapter_generation"],
      "given": "角色 C 处于境界 L",
      "when": "C 与不同境界角色对抗",
      "then": [
        "对低境界：压倒性优势（除非有具体压制原因）",
        "对同境界：胜负取决于具体条件而非光环",
        "对高境界：不应常规取胜",
        "越级击败必须每次都有具体、不可复制的因素"
      ]
    },
    
    {
      "id": "E.1",
      "name": "硬规则不可违反",
      "applies_to": ["graph_construction", "chapter_generation"],
      "given": "规则 R 标注为 hard",
      "when": "任何角色（含主角）触发 R 条件",
      "then": [
        "R.effect 必须生效",
        "不能因剧情需要豁免",
        "若有例外，例外本身必须是规则的一部分"
      ]
    },
    
    {
      "id": "F.1",
      "name": "信息危险性兑现",
      "applies_to": ["chapter_generation"],
      "given": "信息 K 标注 danger_level != safe",
      "when": "角色 C 获得 K",
      "then": [
        "对应的后果必须在合理时间内发生",
        "不能因为 C 是主角豁免"
      ]
    },
    {
      "id": "F.2",
      "name": "跨认知层信息衰减",
      "applies_to": ["chapter_generation"],
      "given": "信息 K 属于认知层 L_high",
      "when": "K 从 L_high 角色传递给 L_low 角色",
      "then": [
        "接收者获得的 K 必须是变质/衰减版本",
        "不能完整传递",
        "若 K.expressible_in_lower_layers == false，传递必失败"
      ]
    },
    {
      "id": "F.3",
      "name": "信息源不可靠性",
      "applies_to": ["chapter_generation"],
      "given": "角色 C 通过来源 S 获得信息 K",
      "when": "S 不是'绝对可靠'级别",
      "then": [
        "C 的视图中 K 必须带不确定性标记",
        "K 在客观图谱中可能为假，且这种'假'应在后续以某种方式揭示"
      ]
    },
    {
      "id": "F.4",
      "name": "不可知层存在性",
      "applies_to": ["full_novel"],
      "given": "图谱中所有视角角色的 cognitive_layer 集合 = {L1, L2, ..., Ln}",
      "when": "检查图谱中的 Knowledge 节点",
      "then": [
        "至少存在一个 Knowledge 节点其 layer > max(L1..Ln)",
        "该 Knowledge 不被任何视角角色 KNOW",
        "读者通过线索能感觉到它存在，但永远拼不出全貌"
      ]
    }
  ],
  
  "validation_workflow": {
    "step_1": "确定产出单元类型（graph_construction | chapter_generation | multi_perspective_chapter | full_novel）",
    "step_2": "筛选 applies_to 包含该类型的场景",
    "step_3": "对每个场景，检查 given 是否成立",
    "step_4": "若 given 成立，验证 then 是否全部满足",
    "step_5": "失败的场景记录到 validation_report",
    "step_6": "若任一相关场景失败，触发重写"
  }
}