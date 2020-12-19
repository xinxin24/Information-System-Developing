from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/course-select")
async def view_list_student_courses(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS cou_sn, term as cou_term, time as cou_time, name as cou_name FROM course ORDER BY name 
        """)
        courses = list(db)

        db.execute("""
        SELECT sel.stu_sn, sel.cou_sn,  
            s.name as stu_name, 
            c.term as cou_term,
            c.name as cou_name,
            c.time as cou_time,
            sel.course_name
        FROM course_sel as sel
            INNER JOIN student as s ON sel.stu_sn = s.sn
            INNER JOIN course as c  ON sel.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'student_course_list.html',
                       students=students,
                       courses=courses,
                       items=items)
                      


@web_routes.get('/course-select/edit/{stu_sn}/{cou_sn}')
def view_student_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT course_name FROM course_sel
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))
  

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, "student_edit.html",
                       stu_sn=stu_sn,
                       cou_sn=cou_sn,
                       #cou_term=cou_term,
                       course_name=record.course_name)


@web_routes.get("/course-select/delete/{stu_sn}/{cou_sn}")
def student_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None :
         return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT sel.stu_sn, sel.cou_sn,
            s.name as stu_name, 
            c.name as cou_name,
            c.term as cou_term,
            c.time as cou_time,
            sel.course_name
        FROM course_sel as sel
            INNER JOIN student as s ON sel.stu_sn = s.sn
            INNER JOIN course as c  ON sel.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))


        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, 'student_dialog.html', record=record)
