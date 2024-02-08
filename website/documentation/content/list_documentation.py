from nicegui import ui

from . import doc


@doc.demo(ui.list)
def main_demo() -> None:
    with ui.list().props('dense separator'):
        with ui.item():
            with ui.item_section():
                ui.item_label('3 Apples')
        with ui.item():
            with ui.item_section():
                ui.item_label('5 Bananas')
        with ui.item():
            with ui.item_section():
                ui.item_label('8 Strawberries')
        with ui.item():
            with ui.item_section():
                ui.item_label('13 Walnuts')


@doc.demo('Use List Items and List Sections to Structure Content', '''
    Items use item sections to structure their content. Item labels take different positions depending on their props.
    ''')
def contact_list():
    with ui.list().props('bordered separator'):
        ui.item_label('Contacts').props('header').classes('text-bold')
        ui.separator()
        with ui.item(on_click=lambda: contact.set_text('Selected contact 1')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('Nice Guy')
                ui.item_label('name').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')
        with ui.item(on_click=lambda: contact.set_text('Selected contact 2')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('Nice Person')
                ui.item_label('name').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')
    contact = ui.label()


doc.reference(ui.list)
