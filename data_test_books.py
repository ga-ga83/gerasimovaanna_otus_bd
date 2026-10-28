import csv
import json

def load_books(csv_path: str):
    books = []
    with open(csv_path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Приводим названия колонок к нижнему регистру для надёжности
            book = {
                "title": row["Title"].strip(),
                "author": row["Author"].strip(),
                "pages": int(row["Pages"]),
                "genre": row["Genre"].strip()
            }
            books.append(book)
    return books

def load_users(json_path: str):
    with open(json_path, mode='r', encoding='utf-8') as f:
        users = json.load(f)
    return users

def distribute_books_evenly(books, users):
    n_books = len(books)
    n_users = len(users)

    if n_users == 0:
        return []

    base_count = n_books // n_users
    remainder = n_books % n_users  # сколько пользователей получат +1 книгу

    distribution = []
    current_index = 0

    for i in range(n_users):
        count = base_count + (1 if i < remainder else 0)
        chunk = books[current_index:current_index + count]
        distribution.append(chunk)
        current_index += count

    return distribution

def main():
    books_file = "books.csv"
    users_file = "users.json"
    result_file = "result.json"

    books = load_books(books_file)
    users = load_users(users_file)

    distributed = distribute_books_evenly(books, users)

    result = []
    for user, user_books in zip(users, distributed):
        user_with_books = dict(user)
        user_with_books["books"] = user_books
        result.append(user_with_books)

    with open(result_file, mode='w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Готово: результат записан в {result_file}")
    print(f"Всего пользователей: {len(users)}, книг: {len(books)}")
    for i, chunk in enumerate(distributed):
        print(f"Пользователь {i}: {len(chunk)} книг")

if __name__ == "__main__":
    main()
