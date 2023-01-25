QUERY_HH = "( Django OR FastAPI OR DRF OR python backend )"

LINK_TO_VACANCIES = (
    "https://api.hh.ru/vacancies?"
    "text={text}&experience={experience}&per_page={per_page}&page={page}&responses_count_enabled=true"
)

LINK_TO_VACANCY = "https://api.hh.ru/vacancies/{vacancy_id}"
EXPERIENCE_NAMES = ["noExperience", "between1And3"]

HH_TEXT_TO_MAILING = """
Добрый день! Прошу рассмотреть мою кандидатуру на данную вакансию.

Если кратко о себе: хорошо знаю Django, DRF, FastAPI(базовые знания), есть опыт работы с celery c брокером Redis, знаю Django ORM, но также умею писать сырые SQL запросы, знаю docker, docker-compose, хорошо знаю git, документирую приложения с помощью swagger.
Базовые знание JavaScript , react , html , css

Ссылка на GitHub - https://github.com/contiinue
По данной ссылке примеры кода.
"""
