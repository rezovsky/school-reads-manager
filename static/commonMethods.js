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

    }
};