new Vue({
    el: '#app',
    data: {
        readers: [
            {
                id: 1,
                first_name: 'John',
                last_name: 'Doe',
                birth_date: '1995-07-15',
                clas: 10,
                class_letter: 'A'
            },
            {
                id: 2,
                first_name: 'Jane',
                last_name: 'Smith',
                birth_date: '2002-03-22',
                clas: 9,
                class_letter: 'B'
            },
        ],
    },
    methods: {
        // Функция для форматирования даты в ДД-ММ-ГГГГ
        formatDate(date) {
            const parts = date.split('-');
            return `${parts[2]}-${parts[1]}-${parts[0]}`;
        },
        // Функция вычисления возраста
        calculateAge(birthDate) {
            const today = new Date();
            const birthDateObj = new Date(birthDate);
            let age = today.getFullYear() - birthDateObj.getFullYear();
            const monthDiff = today.getMonth() - birthDateObj.getMonth();
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
                age--;
            }
            return this.ageWithDeclension(age);
        },
        // Функция склонения подписи к возрасту
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
    },
})

