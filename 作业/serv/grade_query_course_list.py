from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/grade_query_course_list")
async def view_grade_query_course(request):
    return render_html(request, 'grade_query_course_list.html')
    
