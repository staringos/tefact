export interface SharePageEntity {
  type: 'free' | 'password' | 'none';
  password: string;
  key: string;
}
