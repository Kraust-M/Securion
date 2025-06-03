/**
 * Securion - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Password strength meter
    const passwordInput = document.getElementById('password');
    const strengthMeter = document.getElementById('password-strength-meter');
    const strengthText = document.getElementById('password-strength-text');

    if (passwordInput && strengthMeter && strengthText) {
        passwordInput.addEventListener('input', updateStrengthMeter);

        function updateStrengthMeter() {
            const password = passwordInput.value;
            let strength = 0;
            let feedback = '';

            // Length check
            if (password.length >= 8) {
                strength += 1;
            }

            // Contains lowercase letters
            if (password.match(/[a-z]+/)) {
                strength += 1;
            }

            // Contains uppercase letters
            if (password.match(/[A-Z]+/)) {
                strength += 1;
            }

            // Contains numbers
            if (password.match(/[0-9]+/)) {
                strength += 1;
            }

            // Contains special characters
            if (password.match(/[$@#&!]+/)) {
                strength += 1;
            }

            // Update the strength meter
            strengthMeter.value = strength;

            // Update feedback text
            switch (strength) {
                case 0:
                    feedback = 'Very weak';
                    strengthText.className = 'text-danger';
                    break;
                case 1:
                    feedback = 'Weak';
                    strengthText.className = 'text-danger';
                    break;
                case 2:
                    feedback = 'Fair';
                    strengthText.className = 'text-warning';
                    break;
                case 3:
                    feedback = 'Good';
                    strengthText.className = 'text-warning';
                    break;
                case 4:
                    feedback = 'Strong';
                    strengthText.className = 'text-success';
                    break;
                case 5:
                    feedback = 'Very strong';
                    strengthText.className = 'text-success';
                    break;
            }

            strengthText.textContent = feedback;
        }
    }

    // Security assessment form validation
    const assessmentForm = document.getElementById('security-assessment-form');
    if (assessmentForm) {
        assessmentForm.addEventListener('submit', function(event) {
            if (!assessmentForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            assessmentForm.classList.add('was-validated');
        });
    }

    // Security tips filtering
    const categoryFilter = document.getElementById('categoryFilter');
    const difficultyFilter = document.getElementById('difficultyFilter');
    const searchInput = document.getElementById('searchInput');
    const tipCards = document.querySelectorAll('.tip-card');
    
    if (categoryFilter && difficultyFilter && searchInput && tipCards.length > 0) {
        function filterTips() {
            const categoryValue = categoryFilter.value;
            const difficultyValue = difficultyFilter.value;
            const searchValue = searchInput.value.toLowerCase();
            
            tipCards.forEach(card => {
                const category = card.dataset.category;
                const difficulty = card.dataset.difficulty;
                const content = card.textContent.toLowerCase();
                
                const matchesCategory = categoryValue === 'all' || category === categoryValue;
                const matchesDifficulty = difficultyValue === 'all' || difficulty === difficultyValue;
                const matchesSearch = searchValue === '' || content.includes(searchValue);
                
                if (matchesCategory && matchesDifficulty && matchesSearch) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        categoryFilter.addEventListener('change', filterTips);
        difficultyFilter.addEventListener('change', filterTips);
        searchInput.addEventListener('input', filterTips);
    }
}); 