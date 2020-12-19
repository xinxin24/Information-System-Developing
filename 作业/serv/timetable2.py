from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/timetable2")
async def view_timetable_list(request):
    return render_html(request, 'timetable2.html')