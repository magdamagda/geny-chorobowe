function getFilteredDiseases(page) {
    if (page==undefined) {
        page=0;
    }
    window.location.href = 'filterDiseases?diseaseName=' + $("#diseaseName").val() + '&geneSymbol=' + $("#geneSymbol").val()
    + '&fromDate=' + $("#fromDate").val() + '&toDate=' + $("#toDate").val() + '&page=' + page;
    return false;
}

//encodeURIComponent