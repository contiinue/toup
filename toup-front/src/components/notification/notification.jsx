import { useParams } from 'react-router-dom';
import React, { useEffect, useState } from "react"
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import '../../css/notification.css'
import { getCookie } from '../utils/cookies';


function VcancyComponent(props) {
  return (
    <div class="vacancy_container">
      <p><strong>{props.vacancy.name}</strong></p>
      <p><strong>Компания:</strong> {props.vacancy.company_name}</p>
      <p><a href={props.vacancy.alternate_url}>Вакансия</a></p>
    </div>
  )
}


function Notification() {
    const [vacancies, setVacancies] = useState([]);
    let { id } = useParams();
    useEffect(() => {
      async function getVcancies() {
        const response = await fetch(
          `http://127.0.0.1:8000/api/v1/notification/${id}/vacancies_by_notification/`, {
            headers: {
              'Authorization': `Bearer ${getCookie('access')}`,
            }
          })
        const data = await response.json();
        setVacancies(data.vacancies);
      };
      
      getVcancies();
    }, []);
    console.log(vacancies)
    return (
      <div className="container">
        <h1 class='container'>Рассылка: {id}</h1>
          {vacancies.map((vacancy, i) => <VcancyComponent vacancy={vacancy} key={i} />)}
      </div>
    )
}


export default Notification