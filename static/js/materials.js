// materials.js

document.addEventListener('DOMContentLoaded', function () {
    // Only run on materials page
    if (!document.getElementById('materials-search-form')) return;

    const subjectSelect = document.getElementById('filter-subject');
    const gradeSelect = document.getElementById('filter-grade');
    const typeSelect = document.getElementById('filter-type');
    const materialsList = document.getElementById('materials-list');
    const searchForm = document.getElementById('materials-search-form');
    const loadingOverlay = document.getElementById('loading');

    let resourceTypeMap = {};

    function showLoading(show) {
        if (loadingOverlay) loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    function populateDropdown(select, options, placeholder) {
        select.innerHTML = '';
        const defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.textContent = placeholder;
        select.appendChild(defaultOpt);
        options.forEach(opt => {
            const option = document.createElement('option');
            if (typeof opt === 'object') {
                option.value = opt.value;
                option.textContent = opt.label;
            } else {
                option.value = opt;
                option.textContent = opt;
            }
            select.appendChild(option);
        });
    }

    function fetchDropdownOptions() {
        showLoading(true);
        fetch('/api/materials/options/')
            .then(res => res.json())
            .then(data => {
                populateDropdown(subjectSelect, data.subjects, 'All Subjects');
                populateDropdown(gradeSelect, data.grades, 'All Grades');
                populateDropdown(typeSelect, data.types, 'All Types');
                // Build a map for value->label for resource types
                resourceTypeMap = {};
                data.types.forEach(t => { resourceTypeMap[t.value] = t.label; });
            })
            .finally(() => showLoading(false));
    }

    function renderMaterials(materials) {
        if (!materials.length) {
            materialsList.innerHTML = '<div class="alert alert-info">No materials found.</div>';
            return;
        }
        materialsList.innerHTML = materials.map(mat => `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${mat.title}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${mat.subject} | Grade: ${mat.grade} | Type: ${resourceTypeMap[mat.resource_type] || mat.resource_type}</h6>
                    <p class="card-text">${mat.description || ''}</p>
                    ${mat.is_html
                        ? `<a href="/materials/${mat.id}/" target="_blank" class="btn btn-primary">View</a>`
                        : `<a href="${mat.file}" target="_blank" class="btn btn-primary">Download</a>`
                    }
                </div>
            </div>
        `).join('');
    }

    function fetchMaterials() {
        showLoading(true);
        const params = new URLSearchParams();
        const search = document.getElementById('search-query').value.trim();
        if (search) params.append('search', search);
        if (subjectSelect.value) params.append('subject', subjectSelect.value);
        if (gradeSelect.value) params.append('grade', gradeSelect.value);
        if (typeSelect.value) params.append('type', typeSelect.value);
        fetch('/api/materials/filter/?' + params.toString())
            .then(res => res.json())
            .then(renderMaterials)
            .finally(() => showLoading(false));
    }

    // Event listeners
    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        fetchMaterials();
    });
    subjectSelect.addEventListener('change', fetchMaterials);
    gradeSelect.addEventListener('change', fetchMaterials);
    typeSelect.addEventListener('change', fetchMaterials);

    // Initial load
    fetchDropdownOptions();
    fetchMaterials();
}); 