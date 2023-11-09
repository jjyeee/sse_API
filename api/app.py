import re

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_gender = request.form.get("gender")
    return render_template("hello.html", name=input_name, age=input_age,
                           gender=input_gender)


@app.route("/hello_username", methods=["GET"])
def hello_username():
    return render_template("hello_username.html")


def get_content(repo_owner, repo_name):
    content_url = f"\
https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    content_response = requests.get(content_url)

    if content_response.status_code == 200:
        contents = content_response.json()
        content_info = []

        for content in contents:
            content_info.append({
                'name': content['name'],
                'type': content['type'],
                'url': content['url']
            })

        return content_info

    return None


def get_latest_commit(repo_owner, repo_name):
    commit_url = f"https://api.github.co\
m/repos/{repo_owner}/{repo_name}/commits"
    commit_response = requests.get(commit_url)

    if commit_response.status_code == 200:
        commits = commit_response.json()
        if commits:
            latest_commit = commits[0]
            commit_info = {
                'hash': latest_commit['sha'],
                'author': latest_commit['commit']['author']['name'],
                'date': latest_commit['commit']['author']['date'],
                'message': latest_commit['commit']['message'],
                'content': get_content(repo_owner, repo_name)  # 获取文件和目录信息
            }

            return commit_info

    return None


@app.route("/hello_username/response", methods=["POST"])
def response_hello_username():
    username = request.form.get('username')
    github_api_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(github_api_url)

    if response.status_code == 200:
        repos = response.json()
        repo_data = []

        for repo in repos:
            commit_info = get_latest_commit(username, repo['name'])
            if commit_info:
                repo['latest_commit'] = commit_info

            repo_data.append(repo)

        return render_template("hello_username_response.htm\
l", repos=repo_data, username=username)
    else:
        error_message = f"Error fetching repositories for user {username}"
        return render_template("error.html", error=error_message)


@app.route("/query", methods=["GET"])
def query():
    input_query = request.args.get("q")
    return process_query(input_query)


def process_query(input_query):
    if input_query.startswith("What is your name"):
        return "superteam"

    if "dinosaurs" in input_query:
        return "Dinosaurs ruled the Earth 200 \
million years ago"

    if "asteroids" in input_query:
        return "Unknown"

    if input_query.startswith("Which of the following numbers is the largest"):
        result = find_largest_number(input_query)
        return result

    if "plus" in input_query:
        result = add_numbers(input_query)
        return result

    if "minus" in input_query:
        result = subtract_numbers(input_query)
        return result

    if "multiplied" in input_query:
        result = mul_numbers(input_query)
        return result

    if input_query.startswith("Which of the following numbers are primes"):
        result = find_primes(input_query)
        return result


def find_largest_number(query):
    match = re.search(r'(\d+),\s*(\d+),\s*(\d+)', query)

    if match:
        A = int(match.group(1))
        B = int(match.group(2))
        C = int(match.group(3))

        largest = max(A, B, C)
        return str(largest)
    else:
        return "Invalid input"


def subtract_numbers(query):
    match = re.search(r'What is (\d+) minus (\d+)?', query)

    if match:
        A = int(match.group(1))
        B = int(match.group(2))

        result = A - B
        return str(result)
    else:
        return None


def add_numbers(query):
    match = re.search(r'What is (\d+) plus (\d+)?', query)

    if match:
        A = int(match.group(1))
        B = int(match.group(2))

        result = A + B
        return str(result)
    else:
        return None


def mul_numbers(query):
    match = re.search(r'What is (\d+) multiplied by (\d+)?', query)

    if match:
        A = int(match.group(1))
        B = int(match.group(2))

        result = A * B
        return str(result)
    else:
        return None


def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def find_primes(query):
    match = re.search(r'Which of the following \
numbers are primes: (.+)?', query)
    if match:
        numbers_part = match.group(1)
        numbers = [int(num) for num in re.findall(r'\d+', numbers_part)]
        prime_numbers = [num for num in numbers if is_prime(num)]
        return str(prime_numbers)
