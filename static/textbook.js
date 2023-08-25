import commonMethods from './commonMethods.js';

new Vue({
    el: '#app',
    data: {
        moduleName: 'textbook', // название моделя, используется в запросах к API
        moduleData: [], // переменная для хранения списка полученного из API
        moduleDetail: [], // переменная для хранения данных о конкретном элементе списка
        detailId: '', // хранит id элемента списка по которому открываются детальные данные
        moduleKeyName: 'isbn', // имя ключа в данных по которому осуществляется загрузка дитальных данных элемента
        detailData: [], // сюда помещаются данные из списка относящиеся к конкретному элементу
        namesOfField: { // ключи и имена полей списка, ключи соответсвуют ключам данных из API
            isbn: "ISBN",
            title: "Название",
            autor: "Автор",
            year: "Год выпуска",
            clas: "Класс",
            iteration: "Издание",
            publisher: "Издатель",
        },
        newItems: {}, // объект хранит значения для добавляения элемента в список, инициализируется при запуске
        errors: {}, // объект хранит коды ошибок для полей при  добавляения элемента в список, инициализируется при запуске
        editingIndex: null, // переменная для хранения текущего элемента для редактирования в детальной информации
        editedValue: "", // переменная для хранения новой информации для редактирования в детальном списке

        inventCount: 1, // дефолтное значение счетчика для добавления инвентарных номеров
        inventNumber: 0, // дефолтное значение инвентарного номера
        addingInventory: false, // переменная блокировки ввода при добавлении инвентарных номеров до завершения операции

        searchText: '',
    },
    methods: {
        ...commonMethods.methods,

        // Метод для загрузки деталей учебника по ISBN
        loadModuleDetails(id) {
            this.detailId = id; // Устанавливаем текущий ISBN
            this.detailData = this.moduleData.find(item => item[this.moduleKeyName] === id).data;

            // Добавляем новый URL в историю браузера
            window.history.pushState({}, "", `/${this.moduleName}/${id}`);
            this.moduleDetail = []; // Очищаем массив с деталями учебника

            // Добавляем обработчик для события перехода назад в истории браузера
            window.addEventListener("popstate", (event) => {
                this.goBack(); // Вызываем метод для возврата назад
            });

            // Загружаем детали учебника с помощью API запроса
            axios.get(`/api/${this.moduleName}/${id}`)
                .then(response => {
                    this.moduleDetail = response.data;

                    if (this.moduleDetail.length > 0) {
                        this.inventNumber = this.moduleDetail[0].inv.split('.')[0];
                    } else {
                        this.inventNumber = 0;
                    }
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        },
        apiInvent(action, inv = null) {
            if (action === 'add') {
                this.addingInventory = true; // Блокируем элементы ввода
                // Выполнение запроса к API
                axios.post('/api/invent/', {isbn: this.detailId, inv: this.inventNumber, inv_count: this.inventCount})
                    .then(response => {
                        this.moduleDetail = response.data.invs;

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
                        isbn: this.detailId,
                        inv: inv
                    }
                }).then(response => {
                    if (response.status === 204) {
                        // Удаление записи из this.textbookDetail по inv
                        this.moduleDetail = this.moduleDetail.filter(item => item.inv !== inv);

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
            const idIndex = pathSegments.indexOf(this.moduleName) + 1;

            if (idIndex > 0 && idIndex < pathSegments.length) {
                this.detailId = pathSegments[idIndex];
                if (this.detailId) {
                    this.loadModuleDetails(this.detailId); // Вызываем метод для загрузки деталей учебника по ISBN
                }
            }
        });
    },
    mounted() {
        document.body.addEventListener('keydown', this.handleGlobalKeyPress);
    },
    beforeDestroy() {
        document.body.removeEventListener('keydown', this.handleGlobalKeyPress);
    },
    computed: {},
});
