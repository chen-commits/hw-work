tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如北京、上海"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认celsius",
                    },
                    "days": {
                        "type": "integer",
                        "description": "预报天数，1-7之间，默认1",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2+3*4'",
                    },
                    "precision": {"type": "integer", "description": "小数精度，默认2"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "为用户创建一个提醒任务",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "用户ID，例如：user123",
                    },
                    "title": {"type": "string", "description": "提醒标题"},
                    "content": {"type": "string", "description": "提醒详细内容"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "优先级，不提供时默认 medium",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": '标签列表，例如：["工作", "紧急"]',
                    },
                    "time_range": {
                        "type": "object",
                        "description": "提醒的时间范围",
                        "properties": {
                            "start": {
                                "type": "string",
                                "description": "开始时间，格式 HH:MM",
                            },
                            "end": {
                                "type": "string",
                                "description": "结束时间，格式 HH:MM",
                            },
                        },
                    },
                },
                "required": ["user_id", "title", "content"],
            },
        },
    },
]