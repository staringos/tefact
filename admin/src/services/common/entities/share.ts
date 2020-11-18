export interface Share {
  page_id?: string | null;
  type: string;
  password: string | null;
}

export const DefaultShare: Share = {
  page_id: null,
  type: 'password',
  password: null
}
