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
            last_name: "Фамилия",
            first_name: "Имя",
            birth_date: "Дата рождения (ДД.ММ.ГГГГ)",
            clas: "Класс",
            class_letter: "Буква класса",
        },
        newItems: {}, // объект хранит значения для добавляения элемента в список, инициализируется при запуске
        errors: {}, // объект хранит коды ошибок для полей при  добавляения элемента в список, инициализируется при запуске
        editingIndex: null, // переменная для хранения текущего элемента для редактирования в детальной информации
        editedValue: "", // переменная для хранения новой информации для редактирования в детальном списке

        file: null,
        uploadProgress: 0,
        filecomplite: false,
        csvdata: [],
        csvCount: 0,
        filekey: '',
        selectedGroup: null,
        filteredRowCount: 0,
        filterClas: '',
        filterLater: '',

        searchText: '',
    },
    methods: {
        ...commonMethods.methods,

        loadModuleDetails(id) {
            this.detailId = id;
            this.detailData = this.moduleData.readers.find(item => parseInt(item[this.moduleKeyName]) === parseInt(id)).data;


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
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        },
        addBorrowedBook(reader, inv) {
            axios.post(`/api/borrowed/`, {'reader': reader, 'textbook': inv})
                .then(response => {
                    if(response.status === 201){
                        this.loadModuleDetails(reader)
                    }
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        },
        borrowedDel(id, reader) {
            axios.delete(`/api/borrowed/${id}/${reader}/`)
                .then(response => {
                    if (response.status === 204) {
                        this.loadModuleDetails(reader)
                    }
                })
                .catch(error => {
                    console.error('Error fetching books:', error);
                });
        }
        ,
        importCsv() {
            axios.get(`/api/upload/?key=${this.filekey}`).then(
                response => {
                    this.resetModal()
                    this.fetchModuleData()
                })
        }
        ,
        handleFileUpload(event) {
            this.file = event.target.files[0];
            this.uploadFile()
        }
        ,
        uploadFile() {
            if (!this.file) return;

            const formData = new FormData();
            formData.append('file', this.file);
            axios.post('/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: progressEvent => {
                    this.uploadProgress = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                },
            }).then(response => {
                if (response.status === 201) {
                    this.filecomplite = true
                    this.csvdata = response.data.data
                    this.csvCount = response.data.count
                    this.filekey = response.data.key
                } else {
                    console.log('Unexpected response status:', response.status);
                    console.log('Response data:', response.data);
                }
            }).catch(error => {
                console.error('An error occurred:', error);
            });

        }
        ,
        resetModal() {
            this.uploadProgress = 0
            this.filecomplite = false
        }
        ,
        updateSelectedGroup(group) {
            this.selectedGroup = group;
            this.filterClas = group.split(' ')[0]
            this.filterLater = group.split(' ')[1]
            this.filteredRowCount = this.moduleData.readers.filter(reader => (reader.data.clas + ' ' + reader.data.class_letter).includes(group)).length;
        }
        ,
    },
    created() {
        this.initFields()
        this.fetchModuleData().then(() => {

            const path = window.location.pathname;
            const pathSegments = path.split('/');
            const idIndex = pathSegments.indexOf(this.moduleName) + 1;

            if (idIndex > 0 && idIndex < pathSegments.length) {
                this.detailId = pathSegments[idIndex];
                if (this.detailId) {
                    this.loadModuleDetails(this.detailId);
                }
            }
        });

    }
    ,
    mounted() {
        document.body.addEventListener('keydown', this.handleGlobalKeyPress);

    }
    ,
    beforeDestroy() {
        document.body.removeEventListener('keydown', this.handleGlobalKeyPress);
    }
    ,
    computed: {}
    ,
})
;
