from data_types import data_classes


def send_to_channel(project: data_classes.Project):
    post_url = await funcs.send_post(project.id, project.status, project.data)
    await users_db.update_project_post_url(project.id, post_url)
    text = f'<a href="{post_url}">Проект</a> успешно создан'
    await msg.answer(text, reply_markup=markup.main_kb)
