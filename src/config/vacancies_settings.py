LINK_TO_VACANCIES = (
    "https://api.hh.ru/vacancies?"
    "text={text}&experience={experience}&per_page={per_page}&page={page}"
    "&responses_count_enabled=true&professional_role=96"
)

LINK_TO_VACANCY_REQUEST = (
    "https://api.hh.ru/negotiations"
    "?vacancy_id={vacancy_id}&resume_id={resume_id}&message={message}"
)

EXPERIENCE_NAMES = ["noExperience", "between1And3"]

# HH Access errors
ERRORS_TO_CONTINUE = [
    "chat_archived",
    "archived",
    "disabled_by_employer",
    "no_invitation",
    "overall_limit",
    "in_a_row_limit",
    "not_enough_purchased_services",
    "address_not_found",
    "application_denied",
    "edit_forbidden",
    "resume_visibility_conflict",
    "test_required",
    "already_applied",
    "invalid_vacancy",
    "vacancy_not_found",
]

ERRORS_TO_BREAK = [
    "resume_deleted",
    "message_cannot_be_empty",
    "overall_limit",
    "too_long_message",
    "empty_message",
    "wrong_state",
    "limit_exceeded",
    "resume_not_found",
]
