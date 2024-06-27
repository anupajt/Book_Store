<script>
    function updateOrderStatus() {
        setInterval(function () {
            // Make an AJAX request to fetch the latest order status
            $.ajax({
                url: '/get_latest_order_status/',  // Replace with the actual URL
                method: 'GET',
                success: function (data) {
                    // Update the order status in the HTML
                    $('.order-status').text(data.status);
                },
                error: function () {
                    console.error('Failed to fetch order status.');
                }
            });
        }, 5000); // Poll every 5 seconds (adjust as needed)
    }

    // Call the function when the document is ready
    $(document).ready(function () {
        updateOrderStatus();
    });
</script>
