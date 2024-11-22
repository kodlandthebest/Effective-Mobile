import json, os, time

# класс, создающий каждую новую книгу
class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    # метод создаёт словарь из информации о книге, для добавления в .json
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

# класс для первичного создания файла .json и методов его обработки
class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    # загрузка информации из файла .json, если он существует
    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(book_id=book['id'], title=book['title'], author=book['author'], year=book['year'],
                             status=book['status']) for book in data]
        return []

    # сохранение книг в общий словарь с книгами
    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    # добавление книгу с полученными данными в общий словарь с книгами
    def add_book(self, title: str, author: str, year: int):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    # удаление книги по айди
    def remove_book(self, book_id: int):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        raise ValueError("Книга с таким ID не найдена.")

    # поиск книг по названию, автору или году издания
    def search_books(self, query: str):
        results = [book for book in self.books if
                   query.lower() in book.title.lower() or query.lower() in book.author.lower() or query == str(
                       book.year)]
        return results

    # отображение списка книг
    def display_books(self):
        for book in self.books:
            print(
                f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    # смена статуса имеющейся книги с "выдана" на "в наличии" и наоборот
    def change_status(self, book_id: int, new_status: str):
        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Неверный статус. Доступные статусы: 'в наличии', 'выдана'.")
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return
        raise ValueError("Книга с таким ID не найдена.")

# основной цикл приложения, обрабатывающий пользовательский ввод и вызывающий соответствующие методы
def main():
    library = Library('library.json')

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")

        try:
            if choice == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                library.add_book(title, author, year)
            elif choice == '2':
                book_id = int(input("Введите ID книги для удаления: "))
                library.remove_book(book_id)
            elif choice == '3':
                query = input("Введите название, автора или год для поиска: ")
                results = library.search_books(query)
                if results:
                    for book in results:
                        print(
                            f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
                else:
                    print("Книги не найдены.")
            elif choice == '4':
                library.display_books()
            elif choice == '5':
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.change_status(book_id, new_status)
            elif choice == '6':
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")
        except ValueError as e:
            print(f"Ошибка: {e}")

        time.sleep(2)


if __name__ == "__main__":
    main()