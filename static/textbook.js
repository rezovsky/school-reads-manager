new Vue({
  el: '#app',
  data: {
    textbooks: [], // Массив для списка учебников
    textbookDetail: [], // Массив для деталей учебника
    isbn: '', // ISBN текущего учебника
    bookdata: [],
    inventCount: 1,
    inventNumber: 0,
    addingInventory: false,
    yearOptions: [],
    selectedYear: [],
      newTextBookIsbn: '',
      newTextBookTitle: '',
      newTextBookAutor: '',
      newTextBookClas: '',
      newTextBookIteration: '',
      newTextBookPublisher: '',
  newTextBookIsbnError: '',
  newTextBookTitleError: '',
  newTextBookAutorError: '',
  newTextBookYearError: '',
  newTextBookClasError: '',
  newTextBookIterationError: '',
  newTextBookPublisherError: '',
        editingIndex: null,
      editedValue: "",
    namesOfField: {
      "isbn": "ISBN",
      "title": "Название",
      "autor": "Автор",
      "year": "Год выпуска",
      "clas": "Класс",
      "publisher": "Издатель",
    },
  },
  methods: {
    // Метод для загрузки списка учебников
    fetchTextBooks() {
      return axios.get('/api/textbookslist/')
        .then(response => {
          this.textbooks = response.data;
        });
    },
    // Метод для загрузки деталей учебника по ISBN
    loadTextbookDetails(isbn) {
      this.isbn = isbn; // Устанавливаем текущий ISBN
      this.bookdata = this.textbooks.find(textbook => textbook.isbn === isbn).data;

      // Добавляем новый URL в историю браузера
      window.history.pushState({}, "", "/textbook/" + isbn);
      this.textbookDetail = []; // Очищаем массив с деталями учебника

      // Добавляем обработчик для события перехода назад в истории браузера
      window.addEventListener("popstate", (event) => {
        this.goBack(); // Вызываем метод для возврата назад
      });

      // Загружаем детали учебника с помощью API запроса
      axios.get('/api/textbook/' + isbn)
        .then(response => {
          this.textbookDetail = response.data; // Заполняем массив textbookDetail данными из API

          if (this.textbookDetail.length > 0) {
            this.inventNumber = this.textbookDetail[0].inv.split('.')[0];
          } else {
            this.inventNumber = 0;
          }
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    // Метод для возврата к списку учебников
    goBack(event = null) {
        if (event) {
            event.preventDefault();
        }
      history.pushState({}, null, '/textbook/');
      this.isbn = ''; // Очищаем текущий ISBN
      this.textbookDetail = []; // Очищаем массив с деталями учебника
      this.fetchTextBooks()
    },
    focusToElement(targetElement, event = null) {
        if (event && event.keyCode === 9) {
            event.preventDefault();
        }
        this.$refs[targetElement].focus();
    },
    focusToElementFromOpenModal(targetElement) {
        setTimeout(() => {
            this.$refs[targetElement].focus();
        }, 500);
    },
    addTextBook() {
        const newBook = {
          isbn: this.newTextBookIsbn,
          title: this.newTextBookTitle,
          autor: this.newTextBookAutor,
          year: this.selectedYear,
          clas: this.newTextBookClas,
          iteration: this.newTextBookIteration,
          publisher: this.newTextBookPublisher,
        };

        axios.post('/api/textbooks/', newBook) // Замените на ваш адрес API
          .then(response => {
            this.fetchTextBooks().then(() => {
                this.clearModalFields();
                this.closeModal()
                this.loadTextbookDetails(response.data.isbn)
            })
          })
          .catch(error => {
            if (error.response.data){
                this.newTextBookIsbnError = error.response.data.isbn ? error.response.data.isbn[0] : '';
                this.newTextBookTitleError = error.response.data.title ? error.response.data.title[0] : '';
                this.newTextBookAutorError = error.response.data.autor ? error.response.data.autor[0] : '';
                this.newTextBookYearError = error.response.data.year ? error.response.data.year[0] : '';
                this.newTextBookClasError = error.response.data.clas ? error.response.data.clas[0] : '';
                this.newTextBookIterationError = error.response.data.iteration ? error.response.data.iteration[0] : '';
                this.newTextBookPublisherError = error.response.data.publisher ? error.response.data.publisher[0] : '';
            }
          });
      },
    clearModalFields() {
        this.newTextBookIsbn = '';
        this.newTextBookTitle = '';
        this.newTextBookAutor = '';
        this.selectedYear = '';
        this.newTextBookClas = '';
        this.newTextBookIteration = '';
        this.newTextBookPublisher = '';
          this.newTextBookIsbnError = '';
          this.newTextBookTitleError = '';
          this.newTextBookAutorError = '';
          this.newTextBookYearError = '';
          this.newTextBookClasError = '';
          this.newTextBookIterationError = '';
          this.newTextBookPublisherError = '';
    },

toggleEditing(index) {
  this.editingIndex = index;
  this.editedValue = this.bookdata[index];
  setTimeout(() => {
            this.$refs['editing' + index][0].focus();
        }, 100);
},
saveItem(index) {
    const data = {};
    data[index] = this.editedValue;
    axios.put('/api/textbooks/' + this.isbn + '/', data)
          .then(response => {
              this.bookdata[index] = this.editedValue;
              this.editingIndex = null;
          })
          .catch(error => {
            // Обработка ошибки
            console.error('Error adding inventory:', error);
          });
},

    closeModal() {
        document.getElementById('closeModalButton').click();
    },
    selectAllText(event) {
        event.target.select();
    },
    apiInvent(action, inv = null) {

      if (action === 'add') {
        this.addingInventory = true; // Блокируем элементы ввода
        // Выполнение запроса к API
        axios.post('/api/invent/', { isbn: this.isbn, inv: this.inventNumber, inv_count: this.inventCount })
          .then(response => {
            this.textbookDetail = response.data.invs;

            // После выполнения запроса, разблокируем элементы ввода
            this.addingInventory = false;
          })
          .catch(error => {
            // Обработка ошибки
            console.error('Error adding inventory:', error);

            // При ошибке также разблокируем элементы ввода
            this.addingInventory = false;
          });
      } else if (action === 'del' && inv !== null) {
            this.addingInventory = true; // Блокируем элементы ввода
            // Выполнение запроса к API
            axios.delete('/api/invent/', {
                data: {
                    isbn: this.isbn,
                    inv: inv
                }
            }).then(response => {
                if (response.status === 204) {
                    // Удаление записи из this.textbookDetail по inv
                    this.textbookDetail = this.textbookDetail.filter(item => item.inv !== inv);

                    console.log('Record deleted successfully');
                } else {
                    console.log('Unexpected response status:', response.status);
                }

                // После выполнения запроса, разблокируем элементы ввода
                this.addingInventory = false;
            })
              .catch(error => {
                // Обработка ошибки
                console.error('Error adding inventory:', error);

                // При ошибке также разблокируем элементы ввода
                this.addingInventory = false;
          });
      }

    },
  },
  created() {
    this.fetchTextBooks() // Вызов метода для загрузки списка учебников при создании компонента
      .then(() => {
        // Получаем путь URL и извлекаем ISBN из него при создании компонента
        const path = window.location.pathname;
        const pathSegments = path.split('/');
        const isbnIndex = pathSegments.indexOf('textbook') + 1;

        if (isbnIndex > 0 && isbnIndex < pathSegments.length) {
          this.isbn = pathSegments[isbnIndex];
          if (this.isbn) {
            this.loadTextbookDetails(this.isbn); // Вызываем метод для загрузки деталей учебника по ISBN
          }
        }
      });
    const currentYear = new Date().getFullYear();
    for (let i = currentYear; i >= currentYear - 15; i--) {
        this.yearOptions.push(i);
    }
  },
  computed: {

  },
});
