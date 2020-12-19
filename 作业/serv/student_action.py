from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/course-select/add')
async def action_student_course_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    cou_sn = params.get("cou_sn")
    
    #course_name = params.get("course_name")

    if stu_sn is None or cou_sn is None :
        return web.HTTPBadRequest(text="stu_sn, cou_sn must be required")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        #course_name = varchar(course_name)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course_sel (stu_sn, cou_sn) 
            VALUES ( %(stu_sn)s, %(cou_sn)s)
            """, dict(stu_sn=stu_sn, cou_sn=cou_sn))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程",
            "return": "/course-select"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/course-select")


@web_routes.post('/action/course-select/edit/{stu_sn}/{cou_sn}')
async def edit_student_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
   
    if stu_sn is None or cou_sn is None :
        return web.HTTPBadRequest(text="stu_sn, cou_sn,must be required")
  
    params = await request.post()
    course_name = params.get("course_name")
  

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        #course_name = text(course_name)
        
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE course_sel SET course_name=%(course_name)s
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s 
        """, dict(stu_sn = stu_sn, cou_sn=cou_sn, course_name=course_name))

    return web.HTTPFound(location="/course-select")


@web_routes.post('/action/course-select/delete/{stu_sn}/{cou_sn}')
def delete_student_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM course_sel
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))
    return web.HTTPFound(location="/course-select")