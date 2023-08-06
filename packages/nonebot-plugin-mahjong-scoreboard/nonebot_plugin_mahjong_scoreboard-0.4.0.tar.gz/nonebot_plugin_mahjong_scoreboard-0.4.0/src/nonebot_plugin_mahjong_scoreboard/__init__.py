"""
nonebot-plugin-mahjong-scoreboard

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/ssttkkl/nonebot-plugin-mahjong-scoreboard
"""
from nonebot import require

require("nonebot_plugin_localstore")
require("nonebot_plugin_session")
require("nonebot_plugin_sqlalchemy")
require("nonebot_plugin_apscheduler")
require("nonebot_plugin_gocqhttp_cross_machine_upload_file")

from .utils.nonebot import default_cmd_start

help_text = f"""
对局：
- {default_cmd_start}新建对局 [四人南|四人东]
- {default_cmd_start}结算对局 <成绩> [对局<编号>] [@<用户>] [<自风>]
- {default_cmd_start}撤销结算对局 [对局<编号>] [@<用户>]
- {default_cmd_start}设置对局PT <PT> [对局<编号>] [@<用户>]
- {default_cmd_start}删除对局 [对局<编号>]
- {default_cmd_start}设置对局进度 <东/南x局y本场 或 完成> [对局<编号>]

对局查询：
- {default_cmd_start}查询对局 [<编号>]
- {default_cmd_start}个人最近对局 [@<用户>]
- {default_cmd_start}群最近对局
- {default_cmd_start}个人未完成对局 [@<用户>]
- {default_cmd_start}群未完成对局
- {default_cmd_start}导出赛季对局 [<代号>]
- {default_cmd_start}导出所有对局

赛季：
- {default_cmd_start}查询赛季 [<代号>]
- {default_cmd_start}查询所有赛季
- {default_cmd_start}新建赛季
- {default_cmd_start}开启赛季 [<代号>]
- {default_cmd_start}结束赛季
- {default_cmd_start}删除赛季 [<代号>]

赛季查询：
- {default_cmd_start}查询榜单 [<赛季代号>]
- {default_cmd_start}导出榜单 [<赛季代号>]
- {default_cmd_start}查询PT [@<用户>]
- {default_cmd_start}设置PT <PT> [@<用户>]

数据统计：
- {default_cmd_start}对战数据
- {default_cmd_start}赛季对战数据 [<赛季代号>]
- {default_cmd_start}最近走势 [@<用户>]

以上命令格式中，以<>包裹的表示一个参数，以[]包裹的表示一个可选项。

详细说明：参见https://github.com/ssttkkl/nonebot-plugin-mahjong-scoreboard
""".strip()

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='日麻寄分器',
    description='为群友提供日麻计分及榜单统计功能',
    usage=help_text
)

from . import controller
