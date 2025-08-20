// Dashboard Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Pass Django data to JavaScript
    const userData = window.userData || {};
    const courses = window.courses || [];
    const leaderboard = window.leaderboard || [];
    const badges = window.badges || [];
    const weeklyData = window.weeklyData || [];

    // Initialize the dashboard
    try {
        // Log data for debugging
        console.log('userData:', userData);
        console.log('weeklyData:', weeklyData);

        const completionCanvas = document.getElementById('completionChart');
        const weeklyCanvas = document.getElementById('weeklyChart');
        const skillsCanvas = document.getElementById('skillsChart');

        if (completionCanvas && weeklyCanvas && skillsCanvas) {
            initCompletionChart();
            initWeeklyChart();
            initSkillsChart();
        } else {
            console.error('One or more canvas elements not found');
        }
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }

    function initCompletionChart() {
        const ctx = document.getElementById('completionChart').getContext('2d');
        const completionPercent = Number(userData.completionPercentage) || 0;
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Remaining'],
                datasets: [{
                    data: [completionPercent, 100 - completionPercent],
                    backgroundColor: ['#4bc0c0', '#e0e0e0'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: { display: false }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    function initWeeklyChart() {
        const ctx = document.getElementById('weeklyChart').getContext('2d');
        const validData = Array.isArray(weeklyData) ? weeklyData.map(Number) : [0, 0, 0, 0, 0, 0, 0];
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Minutes Learned',
                    data: validData.length >= 7 ? validData.slice(-7) : validData.concat(Array(7 - validData.length).fill(0)),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderRadius: 5
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Minutes'
                        }
                    }
                },
                plugins: {
                    legend: { display: false }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    function initSkillsChart() {
        const ctx = document.getElementById('skillsChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Math', 'Science', 'Writing', 'History', 'Languages'],
                datasets: [{
                    label: 'Skill Level',
                    data: userData.skills || [85, 70, 65, 50, 60], // Use dynamic data or fallback
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                    pointBorderColor: '#fff',
                    pointHoverRadius: 5
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: { display: true },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    legend: { display: false }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Real-time updates
    function updateDashboard() {
        // Update streak counter
        const streakElement = document.getElementById('streakCount');
        if (streakElement) {
            streakElement.textContent = userData.streak || 0;
        }

        // Update points
        const pointsElement = document.getElementById('pointsCount');
        if (pointsElement) {
            pointsElement.textContent = userData.studentpoints || 0;
        }

        // Update level
        const levelElement = document.getElementById('levelCount');
        if (levelElement) {
            levelElement.textContent = userData.level || 1;
        }

        // Update completion percentage
        const completionElement = document.getElementById('completionPercent');
        if (completionElement) {
            completionElement.textContent = userData.completionPercentage || 0;
        }

        // Update XP progress
        const xpProgressBar = document.getElementById('xpProgressBar');
        if (xpProgressBar) {
            const xpPercentage = userData.xpPercentage || 0;
            xpProgressBar.style.width = xpPercentage + '%';
            xpProgressBar.textContent = `${userData.xpProgress || 0}/${userData.xpNeeded || 100} XP`;
        }

        // Update XP needed
        const xpNeededElement = document.getElementById('xpNeeded');
        if (xpNeededElement) {
            xpNeededElement.textContent = userData.xpRemaining || 0;
        }

        // Update today's goals
        const completedGoalsElement = document.getElementById('completedGoals');
        const totalGoalsElement = document.getElementById('totalGoals');
        if (completedGoalsElement && totalGoalsElement) {
            completedGoalsElement.textContent = userData.todayGoal?.completed || 0;
            totalGoalsElement.textContent = userData.todayGoal?.total || 0;
        }

        // Update level display
        const levelDisplayElement = document.getElementById('levelDisplay');
        if (levelDisplayElement) {
            levelDisplayElement.textContent = userData.level || 1;
        }

        // Update user rank
        const userRankElement = document.getElementById('userRank');
        if (userRankElement) {
            userRankElement.textContent = userData.rank || 0;
        }

        // Update user points
        const userPointsElement = document.getElementById('userPoints');
        if (userPointsElement) {
            userPointsElement.textContent = userData.studentpoints || 0;
        }
    }

    // Initialize dashboard updates
    updateDashboard();

    // Set up periodic updates (every 30 seconds)
    setInterval(updateDashboard, 30000);

    // Course card interactions
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        const continueBtn = card.querySelector('.btn');
        if (continueBtn) {
            continueBtn.addEventListener('click', function(e) {
                e.preventDefault();
                const courseTitle = card.querySelector('.card-title').textContent;
                console.log('Continuing course:', courseTitle);
                // Add navigation logic here
                // window.location.href = `/course/${courseId}`;
            });
        }
    });
    document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#student-name').textContent = window.userData.name;
    document.querySelector('#completion').textContent = window.userData.completionPercentage + '%';
    // Update progress bars, charts, etc. using window.courses, window.weeklyData, etc.
});

    // Badge interactions
    const badgeElements = document.querySelectorAll('.custom-badge');
    badgeElements.forEach(badge => {
        badge.addEventListener('click', function() {
            const badgeName = this.querySelector('small').textContent;
            const isEarned = !this.classList.contains('opacity-25');
            
            if (isEarned) {
                // Show badge details
                showBadgeDetails(badgeName);
            } else {
                // Show how to earn badge
                showBadgeRequirements(badgeName);
            }
        });
    });

    function showBadgeDetails(badgeName) {
        // Create modal for badge details
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>${badgeName}</h2>
                <p>Congratulations! You've earned this badge.</p>
                <p>Keep up the great work!</p>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal functionality
        const closeBtn = modal.querySelector('.close');
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }

    function showBadgeRequirements(badgeName) {
        // Create modal for badge requirements
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>${badgeName}</h2>
                <p>Complete the following to earn this badge:</p>
                <ul>
                    <li>Study for 7 consecutive days</li>
                    <li>Complete 10 assignments</li>
                    <li>Score 80% or higher on 5 quizzes</li>
                </ul>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal functionality
        const closeBtn = modal.querySelector('.close');
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }

    // Notification bell functionality
    const notificationBtn = document.querySelector('.btn-outline-light');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            // Toggle notifications panel
            console.log('Opening notifications');
            // window.location.href = '/notifications/';
        });
    }

    // Continue learning button
    const continueLearningBtn = document.querySelector('.btn-primary');
    if (continueLearningBtn) {
        continueLearningBtn.addEventListener('click', function() {
            // Navigate to next lesson or course
            console.log('Continuing learning');
            // window.location.href = '/materials/';
        });
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N for notifications
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            console.log('Opening notifications');
            // window.location.href = '/notifications/';
        }
        
        // Ctrl/Cmd + M for materials
        if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
            e.preventDefault();
            console.log('Opening materials');
            // window.location.href = '/materials/';
        }
    });

    // Add progress animations
    const progressElements = document.querySelectorAll('.progress-bar');
    progressElements.forEach(progress => {
        const width = progress.style.width;
        progress.style.width = '0%';
        
        setTimeout(() => {
            progress.style.transition = 'width 1s ease-in-out';
            progress.style.width = width;
        }, 500);
    });

    // Add achievement notifications
    function showAchievement(message) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-content">
                <i class="fas fa-trophy"></i>
                <span>${message}</span>
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #4ade80, #22c55e);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            font-weight: 600;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Example achievement triggers
    if (userData.streak >= 7) {
        showAchievement('7-day streak! Keep it up!');
    }
    
    if (userData.level > 1) {
        showAchievement(`Level ${userData.level} reached!`);
    }
});
