document.addEventListener('DOMContentLoaded', () => {
    // Ejecutar consulta inicial
    send_query();

    // Añadir evento a los filtros para aplicar automáticamente
    const filters = document.querySelectorAll('#filters input, #filters select, #filters [type="radio"]');
    filters.forEach(filter => {
        filter.addEventListener('input', send_query);
    });

    // Añadir evento al botón "Apply Filters"
    const applyFiltersButton = document.getElementById('apply-filters');
    if (applyFiltersButton) {
        applyFiltersButton.addEventListener('click', send_query);
    }

    // Añadir evento al botón "Clear Filters"
    const clearFiltersButton = document.getElementById('clear-filters');
    if (clearFiltersButton) {
        clearFiltersButton.addEventListener('click', clearFilters);
    }

    // Manejar parámetros de consulta inicial desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    const queryParam = urlParams.get('query');
    if (queryParam && queryParam.trim() !== '') {
        const queryInput = document.getElementById('query');
        queryInput.value = queryParam;
        queryInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
});

function send_query() {
    console.log("Iniciando consulta...");

    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";

    const csrfToken = document.getElementById('csrf_token')?.value || '';

    // Combinar todos los criterios de búsqueda
    const searchCriteria = {
        csrf_token: csrfToken,
        query: document.querySelector('#query').value,
        publication_type: document.querySelector('#publication_type').value,
        sorting: document.querySelector('[name="sorting"]:checked')?.value,
        min_features: document.querySelector('#min_features').value || null,
        max_features: document.querySelector('#max_features').value || null,
        min_products: document.querySelector('#min_products').value || null,
        max_products: document.querySelector('#max_products').value || null,
        after_date: document.querySelector('#after_date').value || null, // Filtros de fechas
        before_date: document.querySelector('#before_date').value || null,
        min_size: parseFloat(document.querySelector('#min_size').value) || null, // Filtros de tamaño
        max_size: parseFloat(document.querySelector('#max_size').value) || null
    };

    console.log("Criterios de búsqueda:", searchCriteria);

    // Realizar la solicitud POST
    fetch('/explore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchCriteria),
    })
        .then(response => {
            console.log("Estado de la respuesta:", response.status);
            if (!response.ok) {
                throw new Error("Error en la respuesta de la solicitud");
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos de respuesta:", data);
            mostrarResultados(data);
        })
        .catch(error => {
            console.error("Error en la solicitud fetch:", error);

            // Recoger los valores de los filtros, incluyendo las fechas y el tamaño
            const searchCriteria = {
                csrf_token: csrfToken,
                query: document.querySelector('#query').value,
                publication_type: document.querySelector('#publication_type').value,
                sorting: document.querySelector('[name="sorting"]:checked').value,
                after_date: document.querySelector('#after_date').value || null,  // Fecha inicial
                before_date: document.querySelector('#before_date').value || null,  // Fecha final
                min_size: parseFloat(document.querySelector('#min_size').value) || null,  // Tamaño mínimo
                max_size: parseFloat(document.querySelector('#max_size').value) || null   // Tamaño máximo
            };

            console.log("Criterios de búsqueda:", searchCriteria);

            fetch('/explore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchCriteria),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Resultados de la búsqueda:", data);
                document.getElementById('results').innerHTML = '';

                // Contador de resultados
                const resultCount = data.length;
                const resultText = resultCount === 1 ? 'dataset' : 'datasets';
                document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

                if (resultCount === 0) {
                    console.log("show not found icon");
                    document.getElementById("results_not_found").style.display = "block";
                } else {
                    document.getElementById("results_not_found").style.display = "none";
                }

                // Generación de las tarjetas de los datasets
                data.forEach(dataset => {
                    let card = document.createElement('div');
                    card.className = 'col-12';
                    card.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex align-items-center justify-content-between">
                                    <h3><a href="${dataset.url}">${dataset.title}</a></h3>
                                    <div>
                                        <span class="badge bg-primary" style="cursor: pointer;" onclick="set_publication_type_as_query('${dataset.publication_type}')">${dataset.publication_type}</span>
                                    </div>
                                </div>
                                <p class="text-secondary">${formatDate(dataset.created_at)}</p>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Description</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        <p class="card-text">${dataset.description}</p>
                                    </div>
                                </div>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Authors</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        ${dataset.authors.map(author => `
                                            <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                        `).join('')}
                                    </div>
                                </div>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Tags</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-md-4 col-12"></div>
                                    <div class="col-md-8 col-12">
                                        <a href="${dataset.url}" class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">View dataset</a>
                                        <a href="/dataset/download/${dataset.id}" class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">Download (${dataset.total_size_in_human_format})</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    document.getElementById('results').appendChild(card);
                });
            });
        });
}

function mostrarResultados(data) {
    const resultsContainer = document.getElementById('results');
    const resultCount = data.length;
    const resultText = resultCount === 1 ? 'dataset' : 'datasets';

    document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

    if (resultCount === 0) {
        console.log("Mostrando icono de no encontrado");
        document.getElementById("results_not_found").style.display = "block";
        return;
    }

    document.getElementById("results_not_found").style.display = "none";

    // Crear y mostrar las tarjetas de los datasets
    data.forEach(dataset => {
        const card = document.createElement('div');
        card.className = 'col-12';
        card.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h3><a href="${dataset.url}">${dataset.title}</a></h3>
                    <p class="text-secondary">${formatDate(dataset.created_at)}</p>
                    <p>${dataset.description}</p>
                    <a href="${dataset.url}" class="btn btn-primary btn-sm">View dataset</a>
                    <a href="/dataset/download/${dataset.id}" class="btn btn-secondary btn-sm">Download (${dataset.total_size_in_human_format})</a>
                </div>
            </div>
        `;
        resultsContainer.appendChild(card);
    });
}

function clearFilters() {
    console.log("Restableciendo filtros...");

    // Resetear la consulta de búsqueda
    document.querySelector('#query').value = "";

    // Resetear tipo de publicación y ordenamiento
    document.querySelector('#publication_type').value = "any";
    document.querySelectorAll('[name="sorting"]').forEach(option => {
        option.checked = option.value === "newest";
    });

    // Resetear filtros de características, productos, fechas y tamaños
    document.querySelector('#min_features').value = "";
    document.querySelector('#max_features').value = "";
    document.querySelector('#min_products').value = "";
    document.querySelector('#max_products').value = "";
    document.querySelector('#after_date').value = "";
    document.querySelector('#before_date').value = "";
    document.querySelector('#min_size').value = "";
    document.querySelector('#max_size').value = "";

    // Ejecutar una nueva consulta con los filtros restablecidos
    send_query();
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('query');
    queryInput.value = tagName.trim();
    send_query();
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    send_query();
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {
    let queryInput = document.querySelector('#query');
    queryInput.value = "";
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any";
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest";
    });

    // Clear the date and size filters
    document.getElementById('after_date').value = "";
    document.getElementById('before_date').value = "";
    document.getElementById('min_size').value = "";
    document.getElementById('max_size').value = "";

    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

document.addEventListener('DOMContentLoaded', () => {
    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (queryParam && queryParam.trim() !== '') {
        const queryInput = document.getElementById('query');
        queryInput.value = queryParam;
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
        console.log("throw event");
    } else {
        const queryInput = document.getElementById('query');
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    }
});

