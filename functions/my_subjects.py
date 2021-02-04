def form_subjects_text(subjects: list) -> str:
    title = '<b>Ваши предметы:</b>'
    subjects = [f' • {s}' for s in subjects]
    result = title + '\n' + '\n'.join(subjects)
    return result
