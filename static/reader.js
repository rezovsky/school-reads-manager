import commonMethods from './commonMethods.js';

new Vue({
    el: '#app',
    data: {
        moduleName: 'reader', // название моделя, используется в запросах к API
        moduleData: [], // переменная для хранения списка полученного из API
        moduleDetail: [], // переменная для хранения данных о конкретном элементе списка
        detailId: '', // хранит id элемента списка по которому открываются детальные данные
        moduleKeyName: 'id', // имя ключа в данных по которому осуществляется загрузка дитальных данных элемента
        detailData: [], // сюда помещаются данные из списка относящиеся к конкретному элементу
        namesOfField: { // ключи и имена полей списка, ключи соответсвуют ключам данных из API
            first_name: "Имя",
            last_name: "Фамилия",
            birth_date: "Дата рождения (ДД-ММ-ГГГГ)",
            clas: "Класс",
            class_letter: "Буква класса",
        },
        newItems: {}, // объект хранит значения для добавляения элемента в список, инициализируется при запуске
        errors: {}, // объект хранит коды ошибок для полей при  добавляения элемента в список, инициализируется при запуске
        editingIndex: null, // переменная для хранения текущего элемента для редактирования в детальной информации
        editedValue: "", // переменная для хранения новой информации для редактирования в детальном списке
    },
    methods: {
        ...commonMethods.methods,

        loadModuleDetails(id) {
            this.detailId = id;
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
    computed: {},
});
