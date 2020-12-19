from aiohttp import web

from serv.config import web_routes, home_path

import serv.error_views
import serv.main_views
import serv.grade_views
import serv.student_views
import serv.student_rest
import serv.course_views
import serv.grade_actions
import serv.course_select
import serv.student_course
import serv.student_action
import serv.timetable1
import serv.timetable2
import serv.grade_query_action
import serv.grade_query_views
import serv.grade_query_student_list
import serv.grade_query_course_list


app = web.Application()
app.add_routes(web_routes)
app.add_routes([web.static("/", home_path / "static")])

if __name__ == "__main__":
    web.run_app(app, port=8080)
