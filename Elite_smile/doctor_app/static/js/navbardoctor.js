function handleSelect(select) {
    const selectedValue = select.value;

    if (selectedValue === "/patient/log_out") {
        select.classList.remove("text-white");
        select.classList.add("text-red-600");

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = selectedValue;

        const csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = '{{ csrf_token }}';
        form.appendChild(csrf);

        document.body.appendChild(form);
        form.submit();
    } else {
        window.location.href = selectedValue;
    }
}