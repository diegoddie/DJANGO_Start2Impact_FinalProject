const eventBox = document.getElementById('event-box-{{ auction.id }}')
const countdownBox = document.getElementById('countdown-box-{{ auction.id }}')

const eventDate = Date.parse(eventBox.textContent)
console.log(eventDate)

setInterval(()=>{
    const now = new Date().getTime()    
    const diff = eventDate - now

    const days = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const hours = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const minutes = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const seconds = Math.floor((eventDate / (1000) - (now / (1000))) % 60)

    if (diff > 0){
        countdownBox.innerHTML = days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds, "
    }else{
    
    }
}, 1000)


