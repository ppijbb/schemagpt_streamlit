const db = require("../../router/config/db");
//pythondata랑 const id = req.body.id;값
insertAFP16 = async (python_data, id) => {
    // var python_data = ['사용자이름','자신의 건강','스트레스5_피로','스트레스3_무기력감','음주여부','음주량',
    // '스트레스2_신경질','여가_중강도 신체활동 여부','스트레스1_긴장, 불안',
    // '스트레스8_대면어려움','규칙적 운동 여부','보조제 복용 유무','스트레스9_시선어려움',
    // 'Vit E(mg)','VitB2(mg)','동물성 단백질(g)','Protein(g)','분류','등급','비질환자 평균'];
    let ID = id['id'];
    let insert_values = [];
    let values = "";
    // 1~16번 insert_values에 넣기
    //console.log("python_data : ",python_data[1]);
    for (let i = 1; i < python_data[1].length - 3; i++) {
      insert_values.push(python_data[1][i]);
    }
    // 1~16번 합계
    let sum = 0;
    insert_values.forEach((item) => {
      sum += Number(item);
    });
    //console.log(sum);
    // 합계에 따른 등급 나누기
    let grade = 0;
    switch (true) {
      case sum > 40:
        grade = 4;
        break;
      case sum > 30:
        grade = 3;
        break;
      case sum > 20:
        grade = 2;
        break;
      default:
        grade = 1;
    }
    // insert문에 넣을 내용
    for (let i = 0; i < insert_values.length; i++) {
      values += Number(insert_values[i]) + ", ";
    }
    //seq 확인
    const select_query = `select SEQ from CARDIO_BASIC where USER_ID='${ID}' ORDER BY SEQ DESC LIMIT 1`;
    db.query(select_query, async function (err, result) {
      if (err) {
        console.log(err);
      }
      //seq가 있는 경우
      if (result.length !==0) {
        result = result[0].SEQ;
        result += 1;
        const query = `insert into CARDIO_BASIC values(${result},'${ID}',${values}${sum}, ${grade}, DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
        db.query(query, function (err, result1) {
          if (err) {
            console.log(err);
          }
        });
      } else { //seq가 없는 경우
        const seq = 1;
        const query = `insert into CARDIO_BASIC values(${seq},'${ID}',${values}${sum}, ${grade}, DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
        db.query(query, function (err, result2) {
          if (err) {
            console.log(err);
          }
        });
      }
    });
  };
  
  //pythondata랑 const id = req.body.id;값
  insertAFP33 = async (python_data, id) => {
    // var python_data = ["사용자이름", "규칙적 운동 여부", "보조제 복용 유무", "스트레스3_무기력감", "스트레스2_신경질", "여가_중강도 신체활동 여부",
    // "자신의 건강", "스트레스5_피로", "음주 여부 및 음주량", "스트레스1_긴장,불안", "스트레스8_대면어려움", "스트레스9_시선어려움",
    // "SBP 2차","DBP 1차","SBP 1차","Vit E(mg)","HDL","LDL","LDL-c","HCT","CHOL","회분(g)","식물성 Fe(mg)","HGB","비만진단-복부지방률",
    // "Mo(ug)","RBC","MONO","VitB2(mg)","동물성 단백질(g)","Cu(ug)","Vit C(mg)","Protein(g)","WBC","신뢰도","등급","비질환자 평균","연속형 분기","방향"];
    // console.log("python_data : ",python_data);
    let ID = id['id'];
    let insert_values = [];
    let values = "";
    for (let i = 1; i < python_data[1].length - 3; i++) {
      insert_values.push(Number(python_data[1][i]));
    }
  
    for (let i = 0; i < insert_values.length; i++) {
      values += Number(insert_values[i]) + ", ";
    }
    var sd = python_data[1][python_data.length - 4];
    var grade = 0;
    switch (sd) {
      case '건강인':
        grade = 0;
        break;
      case '일반인':
        grade = 1;
        break;
      case '위험군':
        grade = 2;
        break;
      default:
        grade = 3;
    }
    values = values + grade;

    const select_query = `select SEQ from CARDIO_DETAIL where USER_ID='${ID}' ORDER BY SEQ DESC LIMIT 1`;
    db.query(select_query,async function (err, result) {
      if (err) {
        console.log(err);
      }
      //seq가 있는 경우
      if (result.length !==0) {
          result = result[0].SEQ;
          result += 1;
        const query = `insert into CARDIO_DETAIL values(${result},'${ID}',${values}, DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
        db.query(query, function (err, result1) {
          if (err) {
            console.log(err);
          }
        });
      } else { //seq가 없는 경우
        const seq = 1;
        const query = `insert into CARDIO_DETAIL values(${seq},'${ID}',${values}, DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
        db.query(query, function (err, result2) {
          if (err) {
            console.log(err);
          }
        });
      }
    });
  };
  
  //raw data 넣기 , const ID = req.body.id;값
  pre_insertAFP33 = async(args, id) => {
    let values = "";
    let ID = id['id'];
    //console.log("args : ",args);
    for(let i=1; i<args.length; i++){
        values += args[i]+", "
    }
    //seq확인
    const select_query = `select SEQ from CARDIO_RAW where USER_ID='${ID}' ORDER BY SEQ DESC LIMIT 1`;
     db.query(select_query, async function (err, result) {
      if (err) {
        console.log(err);
      }
      console.log("result: ",result);
      //seq가 있는 경우
      if (result.length!==0) {
          result = result[0].SEQ;
          result += 1;
        const query = `insert into CARDIO_RAW values(${result},'${ID}',${values} DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
         db.query(query, function (err, result1) {
          if (err) {
            console.log(err);
          }
        });
      } else { //seq가 없는 경우
        const seq = 1;
        const query = `insert into CARDIO_RAW values(${seq},'${ID}',${values} DATE_ADD(NOW(), INTERVAL 9 HOUR))`;
        //   console.log(query);
         db.query(query, function (err, result2) {
          if (err) {
            console.log(err);
          }
        });
      }
    });
  };

  module.exports = {insertAFP16 ,insertAFP33, pre_insertAFP33 };
