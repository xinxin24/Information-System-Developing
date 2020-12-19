from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/grade_query_student_list")
async def view_grade_query_students(request):
    return render_html(request, 'grade_query_student_list.html')
    
