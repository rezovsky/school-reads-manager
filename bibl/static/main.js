new Vue({
    el: '#app',
    data: {
        textbooks: [], // Массив для списка учебников
        textbookDetail: [], // Массив для деталей учебника
        isbn: '', // ISBN текущего учебника
    },
    mounted() {
        this.fetchTextBooks(); // Вызов метода для загрузки списка учебников при монтировании компонента
    },
    methods: {
        // Метод для загрузки списка учебников
        fetchTextBooks() {
            axios.get('/api/textbooks/')
                .then(response => {
                    this.textbooks = response.data; // Заполняем массив textbooks данными из API
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        },
        // Метод для загрузки деталей учебника по ISBN
        loadTextbookDetails(isbn) {
            this.isbn = isbn; // Устанавливаем текущий ISBN
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
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        },
        // Метод для возврата к списку учебников
        goBack() {
            history.pushState({}, null, '/textbook/');
            this.isbn = ''; // Очищаем текущий ISBN
            this.textbookDetail = []; // Очищаем массив с деталями учебника
        },
    },
    created() {
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
    }
});
