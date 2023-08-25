export default {
    methods: {
        focusToElement(targetElement, event = null) {
            if (event && event.keyCode === 9) {
                event.preventDefault();
            }
            this.$refs[targetElement][0].focus();
        },
        handleKeyDown(index, key, event) {
            if (event.key === 'Enter' || event.key === 'Tab') {
                const keys = Object.keys(this.namesOfField);
                const currentIndex = keys.indexOf(key);
                if (currentIndex !== -1) {
                    if (currentIndex === keys.length - 1) {
                        event.preventDefault();
                        this.addItem();
                    } else {
                        const nextKey = keys[currentIndex + 1];
                        this.focusToElement(`${nextKey}Field`, event);
                    }
                }
            }
        },
        focusToElementFromOpenModal(targetElement) {
            setTimeout(() => {
                this.$refs[targetElement][0].focus();
            }, 500);
        },
        closeModal() {
            document.getElementById('closeModalButton').click();
        },
        selectAllText(event) {
            event.target.select();
        },
        clearArray(array) {
            for (const key in array) {
                if (array.hasOwnProperty(key)) {
                    array[key] = '';
                }
            }
        },
        clearModalFields() {
            this.clearArray(this.newItems)
            this.clearArray(this.errors)
        },
        handleErrors(error) {
            if (error.response.data) {

                for (const field in this.namesOfField) {

                    if (this.namesOfField.hasOwnProperty(field)) {
                        const errorData = error.response.data[field];
                        this.$set(this.errors, field, errorData && errorData.length > 0 ? errorData[0] : '');

                    }
                }
            }
        },
        initFields() {
            for (const key in this.namesOfField) {
                if (this.namesOfField.hasOwnProperty(key)) {
                    this.$set(this.newItems, key, '');
                    this.$set(this.errors, key, '');
                }
            }
        },
        fetchModuleData() {
            return axios.get(`/api/${this.moduleName}slist/`)
                .then(response => {
                    this.moduleData = response.data;
                });
        },
        preFetchModuleData() {
            this.fetchModuleData();
            return true;
        },
        // Метод для возврата к списку учебников
        goBack(event = null) {
            if (event) {
                event.preventDefault();
            }
            history.pushState({}, null, `/${this.moduleName}/`);
            this.detailId = '';
            this.moduleDetail = [];
            this.fetchModuleData()
        },
        addItem() {
            axios.post(`/api/${this.moduleName}s/`, this.newItems)
                .then(response => {
                    this.fetchModuleData().then(() => {
                        this.clearModalFields();
                        this.closeModal()
                        this.loadModuleDetails(response.data[this.moduleKeyName])
                    })
                })
                .catch(error => {
                    this.handleErrors(error)
                });
        },
        toggleEditing(index) {
            this.editingIndex = index;
            this.editedValue = this.detailData[index];
            setTimeout(() => {
                this.$refs['editing' + index][0].focus();
            }, 100);
        },
        saveItem(index) {
            const data = {};
            data[index] = this.editedValue;
            axios.put(`/api/${this.moduleName}s/${this.detailId}/`, data)
                .then(response => {
                    this.detailData[index] = this.editedValue;
                    this.editingIndex = null;
                })
                .catch(error => {
                    // Обработка ошибки
                    console.error('Error adding inventory:', error);
                });
        },
        formatDate(date) {
            const parts = date.split('-');
            return `${parts[2]}.${parts[1]}.${parts[0]}`;
        }, // Функция вычисления возраста
        calculateAge(birthDate) {
            const today = new Date();
            const birthDateObj = new Date(birthDate);
            let age = today.getFullYear() - birthDateObj.getFullYear();
            const monthDiff = today.getMonth() - birthDateObj.getMonth();
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
                age--;
            }
            return this.ageWithDeclension(age);
        }, // Функция склонения подписи к возрасту
        ageWithDeclension(age) {
            if (age >= 11 && age <= 14) {
                return `${age} лет`;
            }
            const lastDigit = age % 10;
            if (lastDigit === 1) {
                return `${age} год`;
            } else if (lastDigit >= 2 && lastDigit <= 4) {
                return `${age} года`;
            } else {
                return `${age} лет`;
            }
        },
        getFirstField() {
            return Object.keys(this.namesOfField)[0] + 'Field'
        },
        performSearch() {
            const searchPrefix = this.searchText.substring(0, 3)
            switch (searchPrefix) {
                case '888':
                    if (this.moduleName === "reader" && this.detailId) {
                        const parts = this.searchText.split('-');
                        const inv = `${parts[1]}.${parts[2]}`
                        console.log(`Add book to ${this.detailId}: ${inv}`)
                    }
                    break;
                case '978':
                    if (this.moduleName === 'textbook') {
                        const foundModule = this.moduleData.find(item => item.isbn === this.searchText);
                        if (foundModule) {
                            this.loadModuleDetails(this.searchText)
                        } else {
                            this.newItems.isbn = this.searchText

                            const addTextBookButton = document.getElementById('addTextBookButton');

                            addTextBookButton.click();
                        }
                    }
                    break;
                case '777':
                    if (this.moduleName === "reader") {
                        const parts = this.searchText.split('-');
                        const id = parts[1]
                        const foundModule = this.moduleData.readers.find(item => item.id.toString() === id);
                        if (foundModule) {
                            this.loadModuleDetails(id)
                        }
                    }
                    break;
            }
            this.searchText = ''
        },
        handleGlobalKeyPress(event) {
            const activeElement = document.activeElement;

            if (activeElement.tagName !== 'INPUT') {
                if (
                    event.key.match(/[a-zA-Z0-9.\-]/) &&
                    event.key.length === 1
                ) {
                    this.searchText += event.key;
                }
                if (event.key === 'Enter') {
                    if (this.searchText) {
                        this.performSearch();
                    }
                }
            }
        },

    }
};