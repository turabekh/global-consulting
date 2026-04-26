import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MarketingLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('pages/ProfilePage.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: 'privacy',
        name: 'privacy',
        component: () => import('pages/legal/PrivacyPage.vue'),
      },
      {
        path: 'terms',
        name: 'terms',
        component: () => import('pages/legal/TermsPage.vue'),
      },
      {
        path: 'contact',
        name: 'contact',
        component: () => import('pages/ContactPage.vue'),
      },
      {
        path: 'partnership',
        name: 'partnership',
        component: () => import('pages/PartnershipPage.vue'),
      },
      {
        path: 'about',
        name: 'about',
        component: () => import('pages/AboutPage.vue'),
      },
      {
        path: 'testimonial',
        name: 'testimonial',
        component: () => import('pages/TestimonialsPage.vue'),
      },
      {
        path: 'services',
        name: 'services',
        component: () => import('pages/ServicesPage.vue'),
      },
      {
        path: 'services/:type',
        name: 'service-detail',
        component: () => import('pages/ServiceDetailPage.vue'),
      },
      {
        path: 'blog',
        name: 'blog',
        component: () => import('pages/BlogListPage.vue'),
      },
      {
        path: 'blog/:slug',
        name: 'blog-detail',
        component: () => import('pages/BlogDetailPage.vue'),
      },
    ],
  },
  {
    path: '/dashboard',
    component: () => import('layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('pages/dashboard/DashboardOverviewPage.vue'),
      },
      {
        path: 'applications',
        name: 'applications',
        component: () => import('pages/dashboard/ApplicationListPage.vue'),
      },
      {
        path: 'applications/new',
        name: 'application-new',
        component: () => import('pages/dashboard/ApplicationEditPage.vue'),
      },
      {
        path: 'applications/:reference/edit',
        name: 'application-edit',
        component: () => import('pages/dashboard/ApplicationEditPage.vue'),
      },
    ],
  },
  {
    path: '/',
    component: () => import('layouts/AuthLayout.vue'),
    meta: { guestOnly: true },
    children: [
      { path: 'login', name: 'login', component: () => import('pages/auth/LoginPage.vue') },
      { path: 'signup', name: 'signup', component: () => import('pages/auth/SignupPage.vue') },
      {
        path: 'forgot-password',
        name: 'forgot-password',
        component: () => import('pages/auth/ForgotPasswordPage.vue'),
      },
    ],
  },
  {
    path: '/',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: 'verify-email/:key?',
        name: 'verify-email',
        component: () => import('pages/auth/VerifyEmailPage.vue'),
      },
      {
        path: 'reset-password/:uid/:token',
        name: 'reset-password',
        component: () => import('pages/auth/ResetPasswordPage.vue'),
      },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
