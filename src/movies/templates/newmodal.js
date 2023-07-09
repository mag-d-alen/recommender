

Vue.component = ('CompetitionMultiPlayerSuccessModal',{
template: `
   <div class="competition-modal-content">
            <div class="competition-modal-title">{{ title }}</div>
            <div class = "competition-podium-container">
                <div>{{kvutza.ranking}} place</div>
                <div class="competition-kvutza-name">{{kvutza.name}}</div>
                <div :class=cssClass(kvutza.ranking)></div>
            </div>
   </div>
`,
props:['title','kvutza', 'cssMedalClassMapping'],
methods:{
        cssClass(ranking){ return `podium${ranking}-icon`},
        medalCss(rank){
            return `leaderboard-place-icon ${this.cssMedalClassMapping[rank]}`}
    },
})