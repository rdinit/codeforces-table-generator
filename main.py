import requests


VERDICTS = ["RUNTIME_ERROR", "COMPILATION_ERROR", "WRONG_ANSWER", "MEMORY_LIMIT_EXCEEDED", "TIME_LIMIT_EXCEEDED", "OK"]

with open("codeforces.id") as f:
    CODEFORCES_ID = f.read().replace('\r', '').replace('\n', '')

with open("codeforces_tasks") as f:
    text = f.read().lower().replace('\r', '').split("\n")

TASKS = text[1:]
UNOBLIGATORY_TASKS_COUNT = int(text[0])


def parse_from_cf(codeforces_id) -> list:
    request = requests.get(
        f"https://codeforces.com/api/user.status?handle={codeforces_id}&from=1"
    )
    if request.status_code == 200:
        json_data = request.json()
        if json_data["status"] == "OK":
            return json_data["result"]
        else:
            raise ValueError("Wrong status:" + request.text)
    else:
        raise ValueError(f"request code error. {request.status_code} " + request.text)


def parse_json(attempts) -> dict:
    tasks = dict()
    for attempt in attempts:
        if "++" not in attempt["programmingLanguage"]:
            continue
        task_id = (
            str(attempt["problem"]["contestId"]) + attempt["problem"]["index"].lower()
        )
        if task_id in tasks:
            try:
                tasks[task_id] = max([VERDICTS.index(attempt["verdict"]), tasks[task_id]])
            except ValueError:
                raise ValueError("Wrong verdict type: " + attempt["verdict"])
        else:
            tasks[task_id] = VERDICTS.index(attempt["verdict"])
    return tasks


def generate_markdown(
        obligatory_tasks,
        tasks_solved,
        unobligatory_tasks_count,
        solve_criterion=VERDICTS.index("TIME_LIMIT_EXCEEDED")
    ) -> str:

    table_text = ["Task Id | Status | Obligate |", "|---|---|---|"]
    undrawed_tasks = list(tasks_solved.keys())

    done_obligatory_tasks = 0
    tried_obligatory_tasks = 0
    done_unobligatory_tasks = 0
    tried_unobligatory_tasks = 0

    for task in obligatory_tasks:
        if task in undrawed_tasks:
            if tasks_solved[task] >= solve_criterion:
                done_obligatory_tasks += 1
            tried_obligatory_tasks += 1
            table_text.append(f"|{task}|{VERDICTS[tasks_solved[task]]}|YES|")
            undrawed_tasks.remove(task)
        else:
            table_text.append(f"|{task}| missed |YES|")
    print(undrawed_tasks)
    table_text +=  ["", "Task Id | Status | Obligate |", "|---|---|---|"]
    for task in undrawed_tasks:
        table_text.append(f"|{task}|{VERDICTS[tasks_solved[task]]}|NO|")
        if tasks_solved[task] >= solve_criterion:
            done_unobligatory_tasks += 1
        tried_unobligatory_tasks += 1

    statistics_text = [
        "|name|",
        "|-|",
        f"Obligatory tasks tried: {tried_obligatory_tasks}/{len(obligatory_tasks)} ({int(tried_obligatory_tasks/ len(obligatory_tasks) * 1000) / 10}%)",
        f"Obligatory tasks solved: {done_obligatory_tasks}/{len(obligatory_tasks)} ({int(done_obligatory_tasks/ len(obligatory_tasks) * 1000) / 10}%)",
        f"Unobligatory tasks tried: {tried_unobligatory_tasks}/{unobligatory_tasks_count} ({int(tried_unobligatory_tasks/ unobligatory_tasks_count * 1000) / 10}%)",
        f"Unobligatory tasks solved: {done_unobligatory_tasks}/{unobligatory_tasks_count} ({int(done_unobligatory_tasks/ unobligatory_tasks_count * 1000) / 10}%)",
    ]
    
    return "\n".join(statistics_text + [''] + table_text)


attempts = parse_from_cf(CODEFORCES_ID)
tasks_solved = parse_json(attempts)
markdown = generate_markdown(TASKS, tasks_solved, UNOBLIGATORY_TASKS_COUNT)
with open('cf_status.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
