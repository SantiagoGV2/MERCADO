let map;
let currentMarkerResidencia = null;
let currentMarkerTrabajo = null;
let geocoder;
let autocompleteResidencia;
let autocompleteTrabajo;
let activeField = "residencia"; // Define el campo activo (residencia o trabajo)

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    await google.maps.importLibrary("places");

    // Inicializa el mapa
    map = new Map(document.getElementById("map"), {
        center: { lat: 4.632539102166865, lng: -74.08081778835967 },
        zoom: 12,
    });

    // Inicializa el geocoder
    geocoder = new google.maps.Geocoder();

    // Configura Autocomplete para dirección de residencia
    const direccionInputResidencia = document.getElementById("direccionCasa");
    autocompleteResidencia = new google.maps.places.Autocomplete(direccionInputResidencia);
    autocompleteResidencia.addListener("place_changed", obtenerCoordenadasResidencia);

    // Configura Autocomplete para dirección de trabajo
    const direccionInputTrabajo = document.getElementById("direccionTrabajo");
    autocompleteTrabajo = new google.maps.places.Autocomplete(direccionInputTrabajo);
    autocompleteTrabajo.addListener("place_changed", obtenerCoordenadasTrabajo);

    // Cambia el campo activo cuando se selecciona una entrada
    direccionInputResidencia.addEventListener("focus", () => activeField = "residencia");
    direccionInputTrabajo.addEventListener("focus", () => activeField = "trabajo");

    // Evento al hacer clic en el mapa para seleccionar una ubicación
    map.addListener("click", function (event) {
        const location = event.latLng;

        if (activeField === "residencia") {
            actualizarUbicacionResidencia(location);
        } else if (activeField === "trabajo") {
            actualizarUbicacionTrabajo(location);
        }
    });
}

// Actualiza la ubicación de la residencia
function actualizarUbicacionResidencia(location) {
    // Actualiza los campos de latitud y longitud de residencia
    document.getElementById("latitud").value = location.lat();
    document.getElementById("longitud").value = location.lng();

    // Elimina el marcador actual de residencia si existe
    if (currentMarkerResidencia) {
        currentMarkerResidencia.setMap(null);
    }

    // Crea un nuevo marcador en la ubicación de residencia
    currentMarkerResidencia = new google.maps.Marker({
        position: location,
        map: map,
    });

    // Centra el mapa en la nueva ubicación de residencia
    map.setCenter(location);

    // Obtiene la dirección formateada para la ubicación
    geocoder.geocode({ location: location }, (results, status) => {
        if (status === "OK" && results[0]) {
            document.getElementById("direccionCasa").value = results[0].formatted_address;
        } else {
            alert("No se puede encontrar la dirección para la ubicación de residencia.");
        }
    });
}

// Actualiza la ubicación de trabajo
function actualizarUbicacionTrabajo(location) {
    // Actualiza los campos de latitud y longitud de trabajo
    document.getElementById("latitudTrabajo").value = location.lat();
    document.getElementById("longitudTrabajo").value = location.lng();

    // Elimina el marcador actual de trabajo si existe
    if (currentMarkerTrabajo) {
        currentMarkerTrabajo.setMap(null);
    }

    // Crea un nuevo marcador en la ubicación de trabajo
    currentMarkerTrabajo = new google.maps.Marker({
        position: location,
        map: map,
    });

    // Centra el mapa en la nueva ubicación de trabajo
    map.setCenter(location);

    // Obtiene la dirección formateada para la ubicación
    geocoder.geocode({ location: location }, (results, status) => {
        if (status === "OK" && results[0]) {
            document.getElementById("direccionTrabajo").value = results[0].formatted_address;
        } else {
            alert("No se puede encontrar la dirección para la ubicación de trabajo.");
        }
    });
}

// Función para obtener coordenadas cuando cambia el lugar en Autocomplete para residencia
function obtenerCoordenadasResidencia() {
    const place = autocompleteResidencia.getPlace();

    if (place.geometry) {
        const location = place.geometry.location;
        actualizarUbicacionResidencia(location);
    } else {
        alert("Por favor, selecciona una dirección de residencia válida.");
    }
}

// Función para obtener coordenadas cuando cambia el lugar en Autocomplete para trabajo
function obtenerCoordenadasTrabajo() {
    const place = autocompleteTrabajo.getPlace();

    if (place.geometry) {
        const location = place.geometry.location;
        actualizarUbicacionTrabajo(location);
    } else {
        alert("Por favor, selecciona una dirección de trabajo válida.");
    }
}

initMap();
