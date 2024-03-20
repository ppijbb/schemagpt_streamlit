
const about_Score = function(user_name,grade, result, columns, values, personal){
    let text_item =[[0],[1,2,5,7,8,11],[3,4],[6,9],[10],[12,13,14,15]];
    if (grade === "0") grade = '건강인';
    else if (grade === "1") grade = '일반인';
    else if (grade === "2") grade = '위험군';
    else if (grade === "3") grade = '고위험군';
    user_name = user_name.replace(/"/gi,'')
    values = values.map(x=>Number(x));
    personal = columns[personal].replace(/'/gi,'');
    score0 = values.filter(element => 0 === element).length;
    score1 = values.filter(element => 1 === element).length;
    score2 = values.filter(element => 2 === element).length;
    score3 = values.filter(element => 3 === element).length;

    let empar=[],stress=[],nutr=[];
    let fromIndex = values.indexOf(3);
    
    while(fromIndex != -1)  {
        empar.push(fromIndex);
        fromIndex = values.indexOf(3, fromIndex+1);
      }
    
    for(var i in text_item[1]){
        stress.push(values[text_item[1][i]]);
    }
    for(var i in text_item[5]){
        nutr.push(values[text_item[5][i]]);
    }
    stress = stress.reduce((accumulator, curr) => accumulator + curr);
    nutr = nutr.reduce((accumulator, curr) => accumulator + curr);
    return `'<b>${user_name}</b> 님의 평가 결과는 <b>${result}점</b>으로 <b>${grade}</b>입니다. <br /><br />  0점 ${score0}개, 1점 ${score1}개, 2점 ${score2}개, 3점 ${score3}개로 응답하셨으며,  <b>스트레스</b> 점수(총 18점)는 <b>${stress}점</b>, <b>영양</b> 점수(총 12점)는 <b>${nutr}점</b> 입니다.<br /><br />${dangerscore(empar,columns)}<br /> 비질환자 평균치와 가장 큰 차이를 보이는 항목은 <b>${personal}</b>입니다.'`

    function dangerscore(arr, columns){
        if(arr[0] === undefined) return "<b>위험 점수</b>로 응답한 항목은 <b>없습니다</b>.<br/>"
        else{
            let temparr=""
            for(var i in arr){
                temparr+= '「<b>'+columns[arr[i]].replace(/'/gi,'')+'</b>」, '
            }
            return `<b>위험 점수</b>로 응답한 항목은 ${temparr.slice(0,temparr.length-2)} 입니다.<br />`
        }
    }
}



module.exports.about_Score = about_Score;
