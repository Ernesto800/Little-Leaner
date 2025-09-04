import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import ChatTutor from '@/views/ChatTutor.vue'
import MainMenu from '@/views/MainMenu.vue'
import TinyLesson from '@/views/TinyLesson.vue'
import TinyLessonInside from '@/views/TinyLessonInside.vue'
import PracticaPronunciacion from '@/views/PracticaPronunciacion.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatTutor
    },
    {
      path: '/menu',
      name: 'menu',
      component: MainMenu
    },
    {
      path: '/tinylesson',
      name: 'tinylesson',
      component: TinyLesson
    },
    {
      path: '/tinylesson/:theme/:language',
      name: 'tinylessoninside',
      component: TinyLessonInside,
      props: true,
    },
    {
      path: '/pronouncepractice',
      name: 'pronouncepractice',
      component: PracticaPronunciacion
    }
  ]
})

export default router