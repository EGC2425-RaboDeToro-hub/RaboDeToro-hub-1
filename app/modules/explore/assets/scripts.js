document.addEventListener('DOMContentLoaded', () => {
    send_query();

    // Añadir evento al botón "Apply Filters"
    document.getElementById('apply-filters').addEventListener('click', () => {
        send_query();
    });

    // Añadir evento al botón "Clear Filters"
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
});

function send_query() {
    console.log("Iniciando consulta...");

    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";
    console.log("Ocultar icono de no encontrado");

    const csrfToken = document.getElementById('csrf_token') ? document.getElementById('csrf_token').value : '';

    const searchCriteria = {
        csrf_token: csrfToken,
        query: document.querySelector('#query').value,
        publication_type: document.querySelector('#publication_type').value,
        sorting: document.querySelector('[name="sorting"]:checked').value,
        min_features: document.querySelector('#min_features').value || null,
        max_features: document.querySelector('#max_features').value || null,
        min_products: document.querySelector('#min_products').value || null,
        max_products: document.querySelector('#max_products').value || null
    };

    console.log("Criterios de búsqueda:", searchCriteria);

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
        document.getElementById('results').innerHTML = '';

        // Comprobamos si hay resultados
        const resultCount = data.length;
        const resultText = resultCount === 1 ? 'dataset' : 'datasets';
        document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

        if (resultCount === 0) {
            console.log("Mostrando icono de no encontrado");
            document.getElementById("results_not_found").style.display = "block";
        } else {
            document.getElementById("results_not_found").style.display = "none";
        }

        // Crear y mostrar las tarjetas de los datasets
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
                            <div class="col-md-8 col-12">
                                <a href="${dataset.url}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">
                                    View dataset
                                </a>
                                <a href="/dataset/download/${dataset.id}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">
                                    Download (${dataset.total_size_in_human_format})
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('results').appendChild(card);
        });
    })
    .catch(error => {
        console.error("Error en la solicitud fetch:", error);
    });
}

function formatDate(dateString) {
    const options = {day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric'};
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
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

function clearFilters() {
    console.log("Restableciendo filtros...");

    // Reset the search query
    let queryInput = document.querySelector('#query');
    queryInput.value = "";

    // Reset the publication type to its default value
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any";

    // Reset the sorting option
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest";
    });

    // Reset the additional filters
    document.querySelector('#min_features').value = "";
    document.querySelector('#max_features').value = "";
    document.querySelector('#min_products').value = "";
    document.querySelector('#max_products').value = "";

    // Perform a new search with the reset filters
    send_query();
}
