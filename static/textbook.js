import commonMethods from './commonMethods.js';

new Vue({
    el: '#app',
    data: {
        moduleName: 'textbook',
        moduleData: [], // Массив для списка учебников
        textbookDetail: [], // Массив для деталей учебника
        isbn: '', // ISBN текущего учебника
        bookdata: [],
        inventCount: 1,
        inventNumber: 0,
        addingInventory: false,
        yearOptions: [],
        selectedYear: [],
        namesOfField: {
            isbn: "ISBN",
            title: "Название",
            autor: "Автор",
            year: "Год выпуска",
            clas: "Класс",
            iteration: "Издание",
            publisher: "Издатель",
        },
        newItems: {},
        errors: {},
        editingIndex: null,
        editedValue: "",

    },
    methods: {
        ...commonMethods.methods,

        // Метод для загрузки деталей учебника по ISBN
        loadTextbookDetails(isbn) {
            this.isbn = isbn; // Устанавливаем текущий ISBN
            this.bookdata = this.moduleData.find(textbook => textbook.isbn === isbn).data;

            // Добавляем новый URL в историю браузера
            window.history.pushState({}, "", "/textbook/" + isbn);
            this.textbookDetail = []; // Очищаем массив с деталями учебника

            // Добавляем обработчик для события перехода назад в истории браузера
            window.addEventListener("popstate", (event) => {
                this.goBack(); // Вызываем метод для возврата назад
            });

            // Загружаем детали учебника с помощью API запроса
            axios.get(`/api/${this.moduleName}/` + isbn)
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
            history.pushState({}, null, `/${this.moduleName}/`);
            this.isbn = ''; //
            this.textbookDetail = [];
            this.fetchModuleData()
        },


        addItem() {
            axios.post('/api/textbooks/', this.newItems)
                .then(response => {
                    this.fetchModuleData().then(() => {
                        this.clearModalFields();
                        this.closeModal()
                        this.loadTextbookDetails(response.data.isbn)
                    })
                })
                .catch(error => {
                    this.handleErrors(error)
                });
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
        apiInvent(action, inv = null) {

            if (action === 'add') {
                this.addingInventory = true; // Блокируем элементы ввода
                // Выполнение запроса к API
                axios.post('/api/invent/', {isbn: this.isbn, inv: this.inventNumber, inv_count: this.inventCount})
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
        this.initFields()
        this.fetchModuleData().then(() => {
                // Получаем путь URL и извлекаем ISBN из него при создании компонента
                const path = window.location.pathname;
                const pathSegments = path.split('/');
                const isbnIndex = pathSegments.indexOf(this.moduleName) + 1;

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
    computed: {},
});
