import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {getCookie} from './../utils/cookies'
import '../../css/profile.css'
import { format } from 'date-fns'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';


function GetStatsNotification (props) {
  if (props.status_request) {
    return <div className="notifications_stats">Данные о рассылки: Отправленно: {props.valid_requests} | Проваленно: {props.invalid_requests} </div>
  }
  else {
   return <div className="notifications_stats">Данные о рассылки: Ожидание!</div>
  }
}


function Notifications(props) {
  return (    
    <div className="notification_container">
        <div className="header_notification">
          <div className="date_create_notification">Дата рассылки: {format(new Date(props.notification.date_create), 'yyyy-MM-dd HH:mm')}</div>
          <div className="h6 notification_pk">#{props.notification.pk}</div>
        </div>
        <div className="body_header">
          <div className="body_header_main">
            <div className="">Количество вакансию в рассылке: {props.notification.vacancies.length}</div>
            <div className="status_notification">Статус рассылки: {props.notification.request_notification ? 'Отправленно': 'Не отправленно'}</div>
          </div>
          <div className="body_header_to_notification">
          <a type="button" href={`http://localhost:3000/notification/${props.notification.pk}`} className="btn btn-dark w-100">Перейти к вакансиям</a>
          </div>
        </div>
        <GetStatsNotification valid_requests={props.notification.valid_requests}  invalid_requests={props.notification.invalid_requests} status_request={props.notification.request_notification} /> 
    </div>
  )
}


async function worker_status(status, interval_worker) {
    let response = await fetch('http://127.0.0.1:8000/api/v1/vacancy/worker/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getCookie('access')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'do': status ? 'start': 'stop', 'interval': interval_worker})
    })
    if (response.status == 201) {
      console.log('in f', 'true')
      return true
    }
    else {
      console.log('in f', 'false')
      return false
    }
}


function Worker() {
  let [info, SetInfo] = useState({})
  let [status_worker, SetStatusWorker] = useState(false)
  let [interval_worker, SetIntervalworker] = useState(5)

  useEffect(() => {
    async function getNotifications() {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/vacancy/stats_worker/`, {
        headers: {
          'Authorization': `Bearer ${getCookie('access')}`,
        }
      })
      const data = await response.json();
      SetStatusWorker(data.enabled)
      SetInfo(data);
    };
    
    getNotifications();
  }, []);

  return (
    <div className="worker_container">
      <div className="worker_time_restart h3">Запуск воркера каждые: {info.interval}ч</div>
      <div className="worker_status">Статус: {status_worker ? 'Запущен':'Не запущен'}</div>
      <div className="worker_interval_inuput">
        <input type="number" onChange={(e) => {SetIntervalworker(e.target.value)}} value={interval_worker}/>
      </div>
      <button className="worker_button" onClick={(e) => {SetStatusWorker(!status_worker); worker_status(!status_worker, interval_worker)}}>{status_worker ? 'Остановить':'Запустить'}</button>
    </div>
  )
}

export default function Profile() {
    let { username } = useParams();
    let [notifications, SetNotifications] = useState([]) 

    useEffect(() => {
        async function getNotifications() {
          const response = await fetch(`http://127.0.0.1:8000/api/v1/notification/`, {
            headers: {
              'Authorization': `Bearer ${getCookie('access')}`,
            }
          })
          const data = await response.json();
          SetNotifications(data);
        };
        getNotifications()
      }, []);
    return (
      <div className="container">
        <Worker/>
        <div className="notifications">
          {notifications.map((notification, i) => <Notifications notification={notification} key={i} />)}
        </div>
      </div>
    )
}