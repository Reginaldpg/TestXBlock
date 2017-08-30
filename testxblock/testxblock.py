"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment


class TestXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    has_score = True
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the TestXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/testxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/testxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/testxblock.js"))
        frag.initialize_js('TestXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'
        self.runtime.publish(self, 'grade',
                    { 'value': self.count,
                      'max_value': 100 })
        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def submitanswer(self, data, suffix=''):
        has_score = True
        self.runtime.publish(self, "grade",
                    { 'value': self.count,
                      'max_value': 100 })
        return {"submit" : True}

    @XBlock.json_handler
    def insert_form_data(self, data, suffix=''):
        self.student_score = self.generate_score(data)

        self.runtime.publish(self,'grade',{'value': self.student_score, 'max_value': self.weight})

        if self.first_student:
            self.first_student = False
            self.number_of_headers = data[0]
        
        for index in range(1, len(data)):
            user_data = data[index].encode('ascii', 'replace')
            self.students_form_data.append(user_data)
        
        return {'state': "graded"}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TestXBlock",
             """<testxblock/>
             """),
            ("Multiple TestXBlock",
             """<vertical_demo>
                <testxblock/>
                <testxblock/>
                <testxblock/>
                </vertical_demo>
             """),
        ]
