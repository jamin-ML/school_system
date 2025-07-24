document.addEventListener('DOMContentLoaded', function() {
  // Make footer visible on every page
  var footer = document.querySelector('footer');
  if (footer) {
    footer.classList.add('visible');
  }
  // Utility
  function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) loading.classList.toggle('active', !!show);
  }
  function getToken() {
    return localStorage.getItem('authToken');
  }
  function apiGet(url) {
    return fetch(url, {
      headers: { 'Authorization': 'Token ' + getToken() }
    }).then(r => r.json());
  }
  // Dashboard logic
  if (document.getElementById('dashboard-title')) {
    showLoading(true);
    // Get user info
    apiGet('/api/users/').then(users => {
      // Get current user from token (simulate by fetching /api/users/ and matching by token if needed)
      // For demo, just use the first user
      const user = users[0] || { username: 'User', role: 'student' };
      document.getElementById('user-name').textContent = user.username;
      document.getElementById('role-badge').textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);
      // Fetch dashboard data
      const dashUrl = user.role === 'teacher' ? '/api/dashboard/teacher/' : '/api/dashboard/student/';
      apiGet(dashUrl).then(data => {
        renderDashboardCards(user.role, data);
        if (user.role === 'student') {
          renderFeed('recommendations', data.recommendations || []);
        }
        showLoading(false);
      });
      // Fetch activity feed
      apiGet('/api/activity-feed/').then(feedData => {
        renderFeed('activity-feed', feedData.activity_feed || []);
      });
      // Fetch notifications
      apiGet('/api/notifications/').then(notifs => {
        const unread = (notifs || []).filter(n => !n.read).length;
        document.getElementById('notif-count').textContent = unread > 0 ? unread : '';
      });
    });
  }
  // Render dashboard cards
  function renderDashboardCards(role, data) {
    const cards = [];
    if (role === 'student') {
      // Progress per subject
      (data.progress_per_subject || []).forEach(p => {
        cards.push(`<div class="card"><div class="card-title">${p.subject} Progress</div><div class="card-value">${p.progress}%</div><div class="progress-bar"><div class="progress" style="width:${p.progress}%;"></div></div></div>`);
      });
      // Upcoming assignments
      cards.push(`<div class="card"><div class="card-title">Upcoming Assignments</div><div class="card-value">${(data.upcoming_assignments||[]).length}</div></div>`);
    } else {
      // Teacher: Uploaded resources
      cards.push(`<div class="card"><div class="card-title">Uploaded Resources</div><div class="card-value">${(data.uploaded_resources||[]).length}</div></div>`);
      // Assignment submissions
      cards.push(`<div class="card"><div class="card-title">Assignment Submissions</div><div class="card-value">${(data.assignment_submissions||[]).length}</div></div>`);
      // Student engagement
      if (data.student_engagement) {
        cards.push(`<div class="card"><div class="card-title">Total Views</div><div class="card-value">${data.student_engagement.total_views}</div></div>`);
        cards.push(`<div class="card"><div class="card-title">Total Downloads</div><div class="card-value">${data.student_engagement.total_downloads}</div></div>`);
      }
    }
    document.getElementById('dashboard-cards').innerHTML = cards.join('');
  }
  // Render feed lists
  function renderFeed(id, items) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = items.map(item => {
      if (item.type === 'notification') {
        return `<li><i class="fa-solid fa-bell"></i> ${item.message} <span class="badge">${item.read ? '' : 'New'}</span></li>`;
      } else if (item.type === 'resource_view') {
        return `<li><i class="fa-solid fa-book-open"></i> Viewed: ${item.resource} (${item.subject})</li>`;
      } else if (item.type === 'assignment_submission') {
        return `<li><i class="fa-solid fa-file-arrow-up"></i> Submitted: ${item.assignment} (${item.status})</li>`;
      } else if (item.title && item.subject) {
        // Recommendation
        return `<li><i class="fa-solid fa-lightbulb"></i> ${item.title} <span class="badge">${item.subject}</span></li>`;
      } else {
        return `<li>${item.message || item.title || 'Activity'}</li>`;
      }
    }).join('');
  }
  // Logout
  const logoutBtn = document.getElementById('nav-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      e.preventDefault();
      localStorage.removeItem('authToken');
      window.location.href = '/templates/login.html';
    });
  }
  // --- Materials Page Logic ---
  if (document.getElementById('materials-list')) {
    showLoading(true);
    let allMaterials = [];
    // Fetch all materials
    apiGet('/api/resources/').then(data => {
      allMaterials = data.results || data || [];
      renderMaterials(allMaterials);
      populateFilters(allMaterials);
      showLoading(false);
    });
    // Search/filter logic
    document.getElementById('materials-search-form').addEventListener('submit', function(e) {
      e.preventDefault();
      const q = document.getElementById('search-query').value.toLowerCase();
      const subj = document.getElementById('filter-subject').value;
      const grade = document.getElementById('filter-grade').value;
      const type = document.getElementById('filter-type').value;
      const filtered = allMaterials.filter(m => {
        return (!q || m.title.toLowerCase().includes(q) || m.description.toLowerCase().includes(q)) &&
          (!subj || m.subject === subj) &&
          (!grade || m.grade === grade) &&
          (!type || m.resource_type === type);
      });
      renderMaterials(filtered);
    });
    // Render materials
    function renderMaterials(materials) {
      const list = document.getElementById('materials-list');
      if (!list) return;
      if (!materials.length) {
        list.innerHTML = '<div style="padding:2rem;">No materials found.</div>';
        return;
      }
      list.innerHTML = materials.map(m => `
        <div class="material-card" data-id="${m.id}">
          <div class="material-title">${m.title}</div>
          <div class="material-meta">${m.subject} | Grade ${m.grade} | ${m.resource_type.toUpperCase()}</div>
          <div class="material-meta">Uploaded: ${new Date(m.created_at).toLocaleDateString()}</div>
          <div class="material-status">${m.status.charAt(0).toUpperCase() + m.status.slice(1)}</div>
          <div class="material-actions">
            <button class="btn view-btn">View</button>
          </div>
        </div>
      `).join('');
      // Add click listeners
      document.querySelectorAll('.material-card .view-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const card = btn.closest('.material-card');
          const id = card.getAttribute('data-id');
          const material = materials.find(m => m.id == id);
          openMaterialModal(material);
        });
      });
    }
    // Populate filter dropdowns
    function populateFilters(materials) {
      const subjects = [...new Set(materials.map(m => m.subject))];
      const grades = [...new Set(materials.map(m => m.grade))];
      const types = [...new Set(materials.map(m => m.resource_type))];
      const subjSel = document.getElementById('filter-subject');
      const gradeSel = document.getElementById('filter-grade');
      const typeSel = document.getElementById('filter-type');
      subjects.forEach(s => { if (s) subjSel.innerHTML += `<option value="${s}">${s}</option>`; });
      grades.forEach(g => { if (g) gradeSel.innerHTML += `<option value="${g}">${g}</option>`; });
      types.forEach(t => { if (t) typeSel.innerHTML += `<option value="${t}">${t.toUpperCase()}</option>`; });
    }
    // Modal logic
    const modal = document.getElementById('material-modal');
    const closeModal = document.getElementById('close-modal');
    closeModal.onclick = () => { modal.classList.remove('active'); };
    window.onclick = function(event) { if (event.target == modal) modal.classList.remove('active'); };
    function openMaterialModal(material) {
      modal.classList.add('active');
      document.getElementById('modal-title').textContent = material.title;
      // Viewer
      const viewer = document.getElementById('modal-viewer');
      if (material.resource_type === 'pdf') {
        viewer.innerHTML = `<iframe src="${material.file}" width="100%" height="350px" style="border:none;"></iframe>`;
      } else if (material.resource_type === 'mp4') {
        viewer.innerHTML = `<video controls width="100%"><source src="${material.file}" type="video/mp4"></video>`;
      } else {
        viewer.innerHTML = `<a href="${material.file}" target="_blank">Open File</a>`;
      }
      // Download/pay/question buttons
      const downloadBtn = document.getElementById('download-btn');
      const payBtn = document.getElementById('pay-btn');
      const questionBtn = document.getElementById('question-btn');
      const msg = document.getElementById('modal-message');
      msg.textContent = '';
      if (material.can_download) {
        downloadBtn.style.display = '';
        payBtn.style.display = 'none';
      } else {
        downloadBtn.style.display = 'none';
        payBtn.style.display = '';
      }
      // Download logic
      downloadBtn.onclick = function() {
        showLoading(true);
        fetch(`/api/resources/${material.id}/download/`, {
          headers: { 'Authorization': 'Token ' + getToken() }
        }).then(res => {
          if (res.ok) {
            return res.blob();
          } else {
            return res.json().then(data => { throw new Error(data.detail || 'Download failed'); });
          }
        }).then(blob => {
          showLoading(false);
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = material.title + '.' + material.resource_type;
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
        }).catch(err => {
          showLoading(false);
          msg.textContent = err.message;
        });
      };
      // Pay to download logic (demo: just mark as paid)
      payBtn.onclick = function() {
        showLoading(true);
        fetch(`/api/resources/${material.id}/confirm-payment/`, {
          method: 'POST',
          headers: { 'Authorization': 'Token ' + getToken() }
        }).then(res => res.json()).then(data => {
          showLoading(false);
          if (data.detail && data.detail.includes('Payment confirmed')) {
            msg.textContent = 'Payment successful! You can now download.';
            payBtn.style.display = 'none';
            downloadBtn.style.display = '';
            material.can_download = true;
          } else {
            msg.textContent = data.detail || 'Payment failed.';
          }
        }).catch(() => {
          showLoading(false);
          msg.textContent = 'Payment failed.';
        });
      };
      // Question button (demo: just show a message)
      questionBtn.onclick = function() {
        msg.textContent = 'Feature coming soon!';
      };
    }
  }
  // --- Assignments Page Logic ---
  if (document.getElementById('assignments-list')) {
    showLoading(true);
    let allAssignments = [];
    let userRole = 'student';
    // Get user info
    apiGet('/api/users/').then(users => {
      const user = users[0] || { username: 'User', role: 'student' };
      userRole = user.role;
      // Fetch assignments
      apiGet('/api/assignments/').then(data => {
        allAssignments = data.results || data || [];
        renderAssignments(allAssignments, userRole);
        showLoading(false);
      });
    });
    function renderAssignments(assignments, role) {
      const list = document.getElementById('assignments-list');
      if (!list) return;
      if (!assignments.length) {
        list.innerHTML = '<div style="padding:2rem;">No assignments found.</div>';
        return;
      }
      list.innerHTML = assignments.map(a => `
        <div class="assignment-card" data-id="${a.id}">
          <div class="assignment-title">${a.title}</div>
          <div class="assignment-meta">Due: ${new Date(a.due_date).toLocaleDateString()}</div>
          <div class="assignment-meta">Status: ${a.status.replace('_',' ')}</div>
          <div class="assignment-meta">${a.grade ? 'Grade: ' + a.grade : ''}</div>
          <div class="assignment-status">${a.status.charAt(0).toUpperCase() + a.status.slice(1)}</div>
          <div class="assignment-actions">
            <button class="btn view-assignment-btn">View</button>
          </div>
        </div>
      `).join('');
      document.querySelectorAll('.assignment-card .view-assignment-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const card = btn.closest('.assignment-card');
          const id = card.getAttribute('data-id');
          const assignment = assignments.find(a => a.id == id);
          openAssignmentModal(assignment, role);
        });
      });
    }
    // Modal logic
    const modal = document.getElementById('assignment-modal');
    const closeModal = document.getElementById('close-assignment-modal');
    closeModal.onclick = () => { modal.classList.remove('active'); };
    window.onclick = function(event) { if (event.target == modal) modal.classList.remove('active'); };
    function openAssignmentModal(assignment, role) {
      modal.classList.add('active');
      document.getElementById('assignment-title').textContent = assignment.title;
      document.getElementById('assignment-details').innerHTML = `
        <div><b>Description:</b> ${assignment.description || 'N/A'}</div>
        <div><b>Due Date:</b> ${new Date(assignment.due_date).toLocaleString()}</div>
        <div><b>Status:</b> ${assignment.status.replace('_',' ')}</div>
        <div><b>Grade:</b> ${assignment.grade || 'N/A'}</div>
      `;
      const submissionForm = document.getElementById('submission-form');
      const msg = document.getElementById('submission-message');
      msg.textContent = '';
      if (role === 'student' && (assignment.status === 'not_started' || assignment.status === 'in_progress')) {
        submissionForm.style.display = '';
        submissionForm.onsubmit = function(e) {
          e.preventDefault();
          const fileInput = document.getElementById('submission-file');
          if (!fileInput.files.length) {
            msg.textContent = 'Please select a file.';
            return;
          }
          const formData = new FormData();
          formData.append('assignment', assignment.id);
          formData.append('file', fileInput.files[0]);
          showLoading(true);
          fetch('/api/assignment-submissions/', {
            method: 'POST',
            headers: { 'Authorization': 'Token ' + getToken() },
            body: formData
          }).then(res => res.json()).then(data => {
            showLoading(false);
            if (data.id) {
              msg.textContent = 'Submission successful!';
              submissionForm.style.display = 'none';
            } else {
              msg.textContent = data.detail || 'Submission failed.';
            }
          }).catch(() => {
            showLoading(false);
            msg.textContent = 'Submission failed.';
          });
        };
      } else {
        submissionForm.style.display = 'none';
      }
    }
  }
  // --- Notifications Page Logic ---
  if (document.getElementById('notifications-list')) {
    showLoading(true);
    apiGet('/api/notifications/').then(notifs => {
      renderNotifications(notifs || []);
      showLoading(false);
    });
    function renderNotifications(notifs) {
      const list = document.getElementById('notifications-list');
      if (!list) return;
      if (!notifs.length) {
        list.innerHTML = '<div style="padding:2rem;">No notifications found.</div>';
        return;
      }
      list.innerHTML = notifs.map(n => `
        <div class="notification-item${n.read ? '' : ' unread'}" data-id="${n.id}">
          <i class="fa-solid fa-bell"></i> ${n.message}
          <span style="margin-left:auto;"></span>
          ${n.read ? '' : '<button class="notification-mark-btn">Mark as read</button>'}
        </div>
      `).join('');
      document.querySelectorAll('.notification-mark-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const item = btn.closest('.notification-item');
          const id = item.getAttribute('data-id');
          showLoading(true);
          fetch(`/api/notifications/${id}/read/`, {
            method: 'POST',
            headers: { 'Authorization': 'Token ' + getToken() }
          }).then(res => res.json()).then(() => {
            item.classList.remove('unread');
            btn.remove();
            showLoading(false);
          });
        });
      });
    }
  }
  // --- Profile Page Logic ---
  if (document.getElementById('profile-info')) {
    showLoading(true);
    apiGet('/api/users/').then(users => {
      const user = users[0] || { username: 'User', email: '', role: '', language: 'en' };
      document.getElementById('profile-info').innerHTML = `
        <span><b>Username:</b> ${user.username}</span>
        <span><b>Email:</b> ${user.email}</span>
        <span><b>Role:</b> ${user.role.charAt(0).toUpperCase() + user.role.slice(1)}</span>
        <span><b>Language:</b> ${user.language === 'sw' ? 'Kiswahili' : 'English'}</span>
      `;
      document.getElementById('language-select').value = user.language;
      showLoading(false);
    });
    // Update language
    document.getElementById('language-form').onsubmit = function(e) {
      e.preventDefault();
      const lang = document.getElementById('language-select').value;
      showLoading(true);
      fetch('/api/users/language/', {
        method: 'PATCH',
        headers: {
          'Authorization': 'Token ' + getToken(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ language: lang })
      }).then(res => res.json()).then(data => {
        showLoading(false);
        document.getElementById('profile-message').textContent = 'Language updated!';
      });
    };
    // Change password (demo: just show a message)
    document.getElementById('password-form').onsubmit = function(e) {
      e.preventDefault();
      document.getElementById('profile-message').textContent = 'Password change feature coming soon!';
    };
  }
}); 