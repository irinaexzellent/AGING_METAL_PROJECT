class Utils:

    @staticmethod
    def create_edit_icon(name_table, pk, edit_url='', target_blank=False):
        """
        The method returns 'html' for displaying a pencil icon with a link to the editing page

        """
        edit_icon = '''<span class="act-btn ui-state-default ui-corner-all toolbar-btn"><span class="edit-navi-block ui-icon ui-icon-pencil"></span></span>'''
        target_blank = 'target="_blank"' if target_blank else ""
        html = '<a ' + target_blank + ' href="' + edit_url + str(pk) + '">' + edit_icon + '</a>'
        return html

