$(document).ready(function () {
	$("#site-table").DataTable({
		pageLength: 20,
		lengthMenu: [
			[20, 50, 100, -1],
			[20, 50, 100, "All"],
		],
		autoFill: true,
		order: [],
	});

	document.getElementById("go-url").innerText =
		window.location.href + "go/%s";
});
