$(document).ready(function(){

    function formatDate(date, format) {
        const map = {
            mm: date.getMonth() + 1,
            dd: date.getDate(),
            yy: date.getFullYear().toString(),
            yyyy: date.getFullYear()
        }
    
        return format.replace(/mm|dd|yy|yyy/gi, matched => map[matched])
    }

    const today = new Date();

    // console.log(formatDate(today, 'mm/dd/yy'));

    document.querySelector('.date').value = formatDate(today, 'dd-mm-yy');

    
  
});
  