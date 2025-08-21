export interface Player {
  id: number;
  name: string;
}

export interface User {
  uid: string;
  email: string;
  name?: string;
  customName?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface UserRegistrationData {
  uid: string;
  email: string;
  name: string;
  customName?: string;
}

export interface Companion {
  id: string;
  name: string;
  gender?: string;
  relationship?: string;
  memo?: string;
}