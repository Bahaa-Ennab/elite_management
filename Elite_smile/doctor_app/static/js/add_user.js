$(document).ready(function() {
    // تفعيل select2
    $('#user_id').select2({
        placeholder: "-- اختر المستخدم --",
        dir: "rtl",
        width: '100%'
    });

    // عند تغيير المستخدم
    $('#user_id').change(function() {
        var user_id = $(this).val();
        console.log('Selected User ID:', user_id);

        if (user_id) {
            $.ajax({
                url: user_info_url,  // سيتم تعيينه من القالب
                data: { 'user_id': user_id },
                dataType: 'json',
                success: function(data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $('#email').val(data.email);
                        $('#phone').val(data.phone);
                        $('#role').val(data.role);
                    }
                },
                error: function() {
                    alert('فشل في تحميل البيانات');
                }
            });
        } else {
            $('#email').val('');
            $('#phone').val('');
            $('#role').val('');
        }
    });
});
